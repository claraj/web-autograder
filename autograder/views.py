from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse, HttpResponseBadRequest
from django_eventstream import send_event
from api.models import Grade
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

    # if not request.POST:
    #     # todo make sure at least one student, at least one assignent
    #     # todo can client get error msg?
    #     return HttpResponseBadRequest('No student or assignments provided')

    batch_uuid = uuid.uuid4()

    for assignment in assignments:
        for student in students:
            print('student and assignment ids to queue: ', student, assignment)
            queue_grading_task(batch_uuid, assignment, student)
            # todo reject non-existent students, assignments

    # the response should have the number of existent assignments and students

    return JsonResponse( { 'batch': str(batch_uuid), 'students': len(students), 'assignments': len(assignments) } )


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


# this is not used ATM, replaced with code above.
# def grade(request):
#     if request.method == 'POST':
#         # grade the things
#         json_data = json.loads(request.body)
#         print('the data recd', json_data)
#
#         class GradedAssignments:
#             def __init__(self, assignment, students):
#                 self.student_count = 0
#                 self.students = students
#                 self.asgt = assignment
#             def __iter__(self):
#                 return self
#             def __next__(self):
#                 print('iterator sz next')
#                 if self.student_count >= len(self.students):
#                     raise StopIteration
#
#                 res = autograder.grade(self.asgt, self.students[self.student_count])
#                 self.student_count += 1
#                 return res
#
#
#         # stream response, cuz it's slow
#         streaming_content = GradedAssignments(json_data['assignment'], json_data['students'])
#
#         return StreamingHttpResponse(streaming_content)
#
#     else:
#         assignments = Assignment.objects.order_by('week')
#         students = Student.objects.order_by('name')
#         return render(request, 'autograder/grader.html', { 'students': students, 'assignments': assignments })
