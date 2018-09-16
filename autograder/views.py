from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.db.models import F
import json
from grading_logic import ag as autograder

from .models import Student, Assignment

def home(request):
    return render(request, 'autograder/index.html')
    # if not Student.objects.count() or not Assignment.objects.count():
    #     return HttpResponseRedirect(reverse('create'))
    # return HttpResponseRedirect(reverse('grade'))


# def manage_students(request):
#
#     if request.method == 'GET':
#         students = Student.objects.order_by('name')
#         return render(request, 'autograder/manage_students.html', { 'students': students})
#
#     if request.method == 'PUT':
#         # Should contain all updates to students
#
#         json_data = json.loads(request.body)   # todo errror handling
#         for student_update in json_data['students']:
#             student = Student.objects.get(pk=student_update['pk'])
#             student.org_id = student_update['org_id']
#             student.github_id = student_update['github_id']
#             student.star_id = student_update['star_id']
#             student.name = student_update['name']
#             #student.clean_fields()  # no validation done otherwise.
#             student.save()
#
#         return HttpResponse(status=204)


#     if request.method == 'POST':
#         # json_data = json.loads(request.body)   # todo errror handling
#         # students = json_data['students']
#         # for new_student in students:
#         #     print(new_student)
#         #     student = Student(**new_student)
#         #     student.save()
#         # return HttpResponse(status=201)
#         #
#         #
#
# def manage_assignments(request):
#     return render(request, 'autograder/manage_assignments.html')

def grade(request):
    if request.method == 'POST':
        # grade the things
        json_data = json.loads(request.body)
        print('the data recd', json_data)

        class GradedAssignments:
            def __init__(self, assignment, students):
                self.student_count = 0
                self.students = students
                self.asgt = assignment
            def __iter__(self):
                return self
            def __next__(self):
                print('iterator sz next')
                if self.student_count >= len(self.students):
                    raise StopIteration

                res = autograder.grade(self.asgt, self.students[self.student_count])
                self.student_count += 1
                return res


        # stream response, cuz it's slow
        streaming_content = GradedAssignments(json_data['assignment'], json_data['students'])

        return StreamingHttpResponse(streaming_content)

    else:
        assignments = Assignment.objects.order_by('week')
        students = Student.objects.order_by('name')
        return render(request, 'autograder/grader.html', { 'students': students, 'assignments': assignments })



def results(request, asgt_id):
    # all the results for all students for one week's assignment
    return render(request, 'autograder/results_overview.html')

def assigment_result(request, asgt_id, student_id):
    # results for one student, one assignment
    return render(request, 'autograder/result.html')
