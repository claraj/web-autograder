from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

from .models import Student, Assignment

def home(request):
    return render(request, 'autograder/index.html')
    # if not Student.objects.count() or not Assignment.objects.count():
    #     return HttpResponseRedirect(reverse('create'))
    # return HttpResponseRedirect(reverse('grade'))

def manage_students(request):
    return render(request, 'autograder/manage_students.html')


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
