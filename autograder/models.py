from django.db import models
from django.core.validators import RegexValidator



class ProgrammingClass(models.Model):
    name = models.CharField(max_length=100, default='pants')  # e.g. Java Programming, Programming Logic...
    # Grader - a Python module that knows how to process a GitHub repo, run unit tests, and output a report/questions etc.
    grader = models.CharField(max_length=100)


class Student(models.Model):
    org_id = models.CharField(max_length=8, validators=[RegexValidator('^\d{8}$', message='MCTC Student ID must be 8 numbers')], blank=True)
    name = models.CharField(max_length=200, null=False, blank=False)   # Student real name, as used in D2L
    github_id = models.CharField(max_length=200, blank=True, validators=[RegexValidator('^[\S_-]+$', message='Only letters, numbers, underscores and hyphens.')] )
    star_id = models.CharField(max_length=8, validators=[RegexValidator('^[a-z]{2}\d{4}[a-z]{2}$', message='Star ID must be in the pattern ab1234cd')], blank=True)

    def __str__(self):
        return self.name + ', github ID: ' + self.github_id


class Assignment(models.Model):
    # programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.SET_NULL, null=True)
    week = models.IntegerField()
    github_base = models.CharField(max_length=200)      # e.g. week-0-variables
    instructor_repo = models.CharField(max_length=200)  # eg. https://github.com/minneapolis-edu/JAG_0
    d2l_gradebook_url = models.CharField(max_length=200, blank=True, null=True)


class Grade(models.Model):
    # for an assignment and student
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    generated_report = models.TextField()
    instructor_comments = models.TextField()
    score = models.DecimalField(max_digits=6, decimal_places=3)
