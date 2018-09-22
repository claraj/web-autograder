from django.db import models
from django.core.validators import RegexValidator

# todo better name
class GraderModule(models.Model):
    language = models.CharField(max_length=100)
    module = models.CharField(max_length=100)   # A python module that, when given the instructor code and the student's code, runs the unit tests and outputs a report


class ProgrammingClass(models.Model):
    name = models.CharField(max_length=100, default='spork appreciation 101')  # e.g. Java Programming, Programming Logic...
    semester_code = models.CharField(max_length=6, validators=[RegexValidator('^\d{6}$', message='Must be 6 numbers, year+semester code e.g. Fall 2019 is 201901')])  # summer = 201801, fall = 201803, spring 2019 = 201805
    semester_human_string = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return '%s, %s, %s' % (self.name, self.semester_human_string, self.semester_code)


class Assignment(models.Model):
    programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.DO_NOTHING, blank=True, null=True)
    week = models.IntegerField()
    github_base = models.CharField(max_length=200)      # e.g. week-0-variables
    instructor_repo = models.CharField(max_length=200)  # eg. https://github.com/minneapolis-edu/JAG_0
    d2l_gradebook_url = models.CharField(max_length=200, blank=True, null=False)
    grader = models.ForeignKey(GraderModule, on_delete=models.DO_NOTHING, blank=True, null=True)


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
    assignment = models.ForeignKey(Assignment, on_delete=models.DO_NOTHING, blank=True, null=False)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, blank=True, null=False)
    generated_report = models.TextField()
    instructor_comments = models.TextField()
    score = models.DecimalField(max_digits=6, decimal_places=3)
    # programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.SET_NULL)


class Attributes(models.Model):
    model = models.CharField(max_length=200, null=False, blank=False)  # required
    attr = models.CharField(max_length=200, null=False, blank=False)  # required
    display = models.CharField(max_length=200, null=False, blank=True)  # not required
    validation_regex = models.CharField(max_length=200, null=False, blank=True)  # not required
    validation_fail_message = models.CharField(max_length=200, null=False, blank=True)  # not required
    hyperlink = models.BooleanField(default=False)  # not required
    required = models.BooleanField(default=False)  # not required
    no_edit = models.BooleanField(default=False)  # not required
    omit_from_forms = models.BooleanField(default=False)


      #   attributes: [
      #   { attr: 'id', display: 'id', noEdit: true, omitFromForms: true},
      #   { attr :'week', display: 'Week', regex: /^.+$/, required:true, message: 'Name is required' },
      #   { attr: 'github_base', display: 'GitHub Base', regex: /^[a-zA-Z_\d-]+$/, required: true, message: 'GitHub base can only contain letters, numbers _ and -' },
      #   { attr: 'instructor_repo', display: 'Instructor Repo', required:true, hyperlink: true },
      #   { attr:'d2l_gradebook_url', display: 'D2L Gradebook URL', hyperlink: true },
      #   { attr: 'programming_class', display: 'Class Session'}
      # ],

        # or
        #
        #       attributes: [
        #         { attr: 'id', display: 'id', noEdit: true, omitFromForms: true},
        #         { attr :'name', display: 'Name', regex: /^.+$/, required:true, message: 'Name is required' },
        #         { attr: 'github_id', display: 'Github ID', regex: /^[a-zA-Z_\d-]+$/, message: 'GitHub username can only contain letters, numbers _ and -' },
        #         { attr: 'org_id', display: 'MCTC ID', regex: /^\d{8}$/, message: 'MCTC id should be 8 numbers' },
        #         { attr:'star_id', display:'Star ID', regex: /^[a-z]{2}\d{4}[a-z]{2}$/, message: 'Star ID must be in the form ab1234cd' },
        #         { attr: 'programming_class', display: 'Class Session'}
        #       ],