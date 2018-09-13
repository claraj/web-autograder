from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import F

from .models import Student, Assignment

def home(request):
    return render(request, 'autograder/index.html')
    # if not Student.objects.count() or not Assignment.objects.count():
    #     return HttpResponseRedirect(reverse('create'))
    # return HttpResponseRedirect(reverse('grade'))


def manage_students(request):

    if request.method == 'GET':
        students = Student.objects.all()
        return render(request, 'autograder/manage_students.html', {students: students})
    if request.method == 'PUT':
        # Should contain all updates to students
        for student_update in request.PUT:
            student = Students.objects.get(pk=student.pk)
            student.org_id = student_update['org_id']
            student.github_id = student_update['github_id']
            student.star_id = student_update['star_id']
            student.name = student_update['name']
            student.save()
        return redirect(reverse('manage_students'))
    if request.method == 'POST':
        for new_student in request.PUT:
            student = Student(new_student)
            student.save()
        return redirect(reverse('manage_students'))



def manage_assignments(request):
    return render(request, 'autograder/manage_assignments.html')

def grade(request):
    return render(request, 'autograder/grader.html')

def results(request, asgt_id):
    # all the results for all students for one week's assignment
    return render(request, 'autograder/results_overview.html')

def assigment_result(request, asgt_id, student_id):
    # results for one student, one assignment
    return render(request, 'autograder/result.html')
