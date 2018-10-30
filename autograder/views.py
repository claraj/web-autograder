from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse, HttpResponseBadRequest
from django_eventstream import send_event
from api.models import Grade, GradingBatch
import uuid
import json

from .grading_queue import queue_grading_task



@require_http_methods('POST')
def grader_start(request):
    # todo only post

    """
    Make a UUId for all the graded things in this batch
    make a task for each student & assignment and dump into queue
    return UUID for client to use to query progress
    """

    body = json.loads(request.body)

    students = body.get('students')
    assignments = body.get('assignments')
    programming_class = body.get('programming_class')

    # if not request.POST:
    #     # todo make sure at least one student, at least one assignent
    #     # todo can client get error msg?
    #     return HttpResponseBadRequest('No student or assignments provided')


    batch_uuid = uuid.uuid4()

    no_students = len(students)
    no_assignments = len(assignments)

    batch = GradingBatch(id = batch_uuid, things_to_grade=(no_students * no_assignments))
    batch.save()

    for assignment in assignments:
        for student in students:
            print('student and assignment ids to queue: ', student, assignment)
            queue_grading_task(batch_uuid, assignment, student, programming_class)
            # todo reject non-existent students, assignments

    # the response should have the number of existent assignments and students

    return JsonResponse( { 'batch': str(batch_uuid), 'students': no_students, 'assignments': no_assignments, 'programming_class': programming_class } )


def grader_get_progress(request):

    """
    Make a UUId for all the graded things in this batch
    make a task for each student & assignment and dump into celery/huey/djangoQ queue
    return UUID for client to use to query progress

    Return a list of assignments IDs that are graded in this batch. Client can figure out which ones
    it doesn't know about yet and query the API to get the full info for each assignment.

    """

    batch = request.GET.get('batch')
    if not batch:
        # 404
        print('no batch')
        return HttpResponseBadRequest('No grading batch provided')

    grading_batch = Grade.objects.filter(batch=batch)

    graded_ids = [ object.id for object in grading_batch ]

    print(graded_ids)

    return JsonResponse( { 'graded_ids' : graded_ids })
