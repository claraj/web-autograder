from django.db import models
from django.core.validators import RegexValidator
from students.models import Student
from assignments.models import Assignment


class ProgrammingClass(models.Model):
    name = models.CharField(max_length=100, default='pants')  # e.g. Java Programming, Programming Logic...

    # Grader - TODO  will be a Python module that knows how to process a GitHub repo, run unit tests, and output a report/questions etc.
    grader = models.CharField(max_length=100)


class Grade(models.Model):
    # for an assignment and student
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    generated_report = models.TextField()
    instructor_comments = models.TextField()
    score = models.DecimalField(max_digits=6, decimal_places=3)
