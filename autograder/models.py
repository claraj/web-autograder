from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Student(models.Model):
    student_id = models.CharField(max_length=8, validators=[RegexValidator('^\d{8}$', message='MCTC Student ID must be 8 numbers')])
    name = models.CharField(max_length=200)
    github_name = models.CharField(max_length=200)
    star_id = models.CharField(max_length=8, validators=[RegexValidator('^[a-z]{2}\d{4}[a-z]{2}$', message='Star ID must be in the pattern ab1234cd')])

    def __str__(self):
        return self.name + ' ' + self.github_name
