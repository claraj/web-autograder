from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse, HttpResponseBadRequest
from django_eventstream import send_event
from api.models import Grade, GradingBatch
import uuid
import json
import logging
from django.shortcuts import get_object_or_404

from .grading_queue import queue_grading_task


@require_http_methods('POST')
def grader_start(request):

    """
    Make a UUId for all the graded things in this batch
    make a task for each student & assignment and dump into queue
    return batch UUID for client to use to query progress
    """

    body = json.loads(request.body)

    students = body.get('students')
    assignments = body.get('assignments')
    programming_class = body.get('programming_class')

    if not students or not assignments or not programming_class:
        return HttpResponseBadRequest('Provide at least one assignment, one student, one programing class.')

    batch_uuid = uuid.uuid4()

    no_students = len(students)
    no_assignments = len(assignments)

    things_to_grade = 0

    for assignment in assignments:
        for student in students:
            logging.info(f'ids for queue: student {student}, assignment {assignment}, class {programming_class}')

            try:
                queue_grading_task(batch_uuid, assignment, student, programming_class)
                things_to_grade += 1
            except Exception as e:
                # Errors on non-existent students, assignments
                logging.warning(f'Error queueing grading task for student {student}, assignment {assignment}, class {programming_class}, because {e}. skipping')

    batch = GradingBatch(id = batch_uuid, things_to_grade=things_to_grade)
    batch.save()

    return JsonResponse( { 'batch': str(batch_uuid), 'items_to_grade': things_to_grade, 'students': no_students, 'assignments': no_assignments, 'programming_class': programming_class } )


def grader_get_progress(request):

    """
    Return a list of assignments IDs that are graded in this batch. Client can figure out which ones
    it doesn't know about yet and query the API to get the full info for each assignment.
    """

    batch = request.GET.get('batch')
    if not batch:
        return HttpResponseBadRequest('No grading batch provided')

    grading_batch = Grade.objects.filter(batch=batch)
    graded_ids = [ object.id for object in grading_batch ]
    return JsonResponse( { 'graded_ids' : graded_ids })


@require_http_methods('POST')
def regrade(request):

    """ Convenience method to run the grader for a Grade object """
    body = json.loads(request.body)
    id = body.get('id')
    if not id:
        return HttpResponseBadRequest('No id provided')
    batch_uuid = uuid.uuid4()
    grade = get_object_or_404(Grade, id=id)
    batch = GradingBatch(batch_uuid, things_to_grade=1)
    batch.save()
    queue_grading_task(batch_uuid, grade.assignment.id, grade.student.id, grade.programming_class.id)
    return JsonResponse( {'batch': str(batch_uuid), 'items_to_grade': 1, 'no_students': 1, 'no_assignments': 1, 'programming_class': grade.programming_class.id})


@require_http_methods('GET')
def textReport(request, pk):
    """ Generate a report formated as a single block of text, intended for copying into D2L """

    # return JsonResponse({'text': 'HELLO!'})
    grade = get_object_or_404(Grade, pk=pk)
    report = json.loads(grade.generated_report)
    score = '{:.2f}'.format(grade.score)

    # Errored?
    if 'error' in report:
        error_str = report['error']
        report = f'Could not run code, {error_str}. \nGrade is {score}'
        return JsonResponse({'text': report})

    q_message = ''

    for q in report['question_reports']:
        q_number = q['question']['question']
        points_avail = q['question']['points']
        points_earned = q['points_earned']
        sourcefile = q['question']['source_file']
        tests = q['tests']
        passes = q['passes']

        q_message += f'Question {q_number}, from file {sourcefile}\n'

        for testsuites in q['testsuites']:
            tsname = testsuites['name']
            ts_f = testsuites['failures']
            ts_t = testsuites['tests']
            ts_s = testsuites['skipped']
            ts_e = testsuites['errors']

            if ( ts_f + ts_e + ts_s) == 0: # all passed
                q_message += f'{tsname}: all {ts_f} tests passed\n'
                continue

            for testsuite in testsuites['testsuites']:

                q_message += f'Testsuite {testsuite["name"]}\n'

                for testcase in testsuite['testcases']:
                    passed = testcase['passed']
                    tcname = testcase['name']
                    if passed:
                        q_message += f' * {tcname} passed\n'

                    if testcase['error']:
                        q_message += f' * {tcname} errored because {testcase["error"]["message"]}\n'
                    if testcase['failure']:
                        q_message += f' * {tcname} failed because {testcase["failure"]["message"]}\n'

        q_message += f'Points available {points_avail}, points earned {points_earned}\n\n'


    overall = report.get('overall_instructor_comments\n', '')
    outline = f'{q_message}{overall}Autograded score {score}'


    return JsonResponse({'text': outline})
