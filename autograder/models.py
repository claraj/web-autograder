from django.db import models
from django.core.validators import RegexValidator


class ProgrammingClass(models.Model):
    name = models.CharField(max_length=100, default='spork appreciation 101')  # e.g. Java Programming, Programming Logic...
    semester_code = models.CharField(max_length=6)  # summer = 201801, fall = 201803, spring 2019 = 201805


class Assignment(models.Model):
    programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.DO_NOTHING, null=True, blank=True)
    week = models.IntegerField()
    github_base = models.CharField(max_length=200)      # e.g. week-0-variables
    instructor_repo = models.CharField(max_length=200)  # eg. https://github.com/minneapolis-edu/JAG_0
    d2l_gradebook_url = models.CharField(max_length=200, blank=True, null=False)
    grader = models.ForeignKey('autograder.GraderModule', on_delete=models.DO_NOTHING)


class Student(models.Model):
    programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.DO_NOTHING, null=True, blank=True)
    org_id = models.CharField(max_length=8, validators=[RegexValidator('^\d{8}$', message='MCTC Student ID must be 8 numbers')], null=False, blank=True)
    name = models.CharField(max_length=200, null=False, blank=False)   # Student real name, as used in D2L
    github_id = models.CharField(max_length=200, blank=True, null=False, validators=[RegexValidator('^[\S_-]+$', message='Only letters, numbers, underscores and hyphens.')] )
    star_id = models.CharField(max_length=8, validators=[RegexValidator('^[a-z]{2}\d{4}[a-z]{2}$', message='Star ID must be in the pattern ab1234cd')], null=False, blank=True)

    def __str__(self):
        return 'Name: %s, GitHub ID: %s ' % (self.name, self.github_id)


class Grade(models.Model):
    # for an assignment and student. The assignment knows what programming class it belongs to.
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    generated_report = models.TextField()
    instructor_comments = models.TextField()
    score = models.DecimalField(max_digits=6, decimal_places=3)
    # programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.SET_NULL)

# todo better name
class GraderModule(models.Model):
    language = models.CharField(max_length=100)
    module = models.CharField(max_length=100)   # A python module that, when given the instructor code and the student's code, runs the unit tests and outputs a report
