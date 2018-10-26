from django.db import models
from django.core.validators import RegexValidator


class ProgrammingClass(models.Model):
    name = models.CharField(max_length=100, default='spork appreciation 101')  # e.g. Java Programming, Programming Logic...
    semester_code = models.CharField(max_length=6, validators=[RegexValidator('^\d{6}$', message='Must be 6 numbers, year+semester code e.g. Fall 2019 is 201901')])  # summer = 201801, fall = 201803, spring 2019 = 201805
    semester_human_string = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return '%s, %s, %s' % (self.name, self.semester_human_string, self.semester_code)


class Assignment(models.Model):
    programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.PROTECT, blank=True, null=True)
    week = models.IntegerField()
    github_base = models.CharField(max_length=200)      # e.g. week-0-variables
    github_org = models.CharField(max_length=200)
    instructor_repo = models.CharField(max_length=200)  # eg. https://github.com/minneapolis-edu/JAG_0
    d2l_gradebook_url = models.CharField(max_length=200, blank=True, null=False)

    class Meta:
        unique_together = ( ('week', 'programming_class'), )

    def __str__(self):
        return 'Class: [%s] Week: [%d] GitHub Base: [%s] Intructor Repo: [%s] D2L URL [%s] ' % (self.programming_class, self.week, self.github_base, self.instructor_repo, self.d2l_gradebook_url)


class Student(models.Model):
    programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.PROTECT, null=True, blank=True)
    org_id = models.CharField(max_length=8, validators=[RegexValidator('^\d{8}$', message='MCTC Student ID must be 8 numbers')], null=False, blank=True)
    name = models.CharField(max_length=200, null=False, blank=False)   # Student real name, as used in D2L
    github_id = models.CharField(max_length=200, blank=True, null=False, validators=[RegexValidator('^[\S_-]+$', message='Only letters, numbers, underscores and hyphens.')] )
    star_id = models.CharField(max_length=8, validators=[RegexValidator('^[a-z]{2}\d{4}[a-z]{2}$', message='Star ID must be in the pattern ab1234cd')], null=False, blank=True)
    active = models.BooleanField(default=True)   # becomes False if student drops, withdraws, is abducted by aliens etc.

    def __str__(self):
        return 'Name: %s, GitHub ID: %s ' % (self.name, self.github_id)


class Grade(models.Model):
    # for an assignment and student. The assignment knows what programming class it belongs to.
    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT, blank=False, null=False)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, blank=False, null=False)
    generated_report = models.TextField(blank=True, null=True)
    instructor_comments = models.TextField(blank=True, null=True)
    score = models.DecimalField(max_digits=6, decimal_places=3)
    student_github_url = models.CharField(max_length=400, blank=True)
    batch = models.UUIDField()
    github_commit_hash = models.CharField(max_length=40, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True)
    # programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.SET_NULL)
    error = models.TextField(blank=True, null=True)  # errors from grading process, could be programatic errors
    reviewed = models.BooleanField(default=False, blank=True, null=False)

    def __str__(self):
        return 'assignment %s student %s batch %s date %s, score %f'  % (self.assignment.id, self.student.id, self.batch, self.date, self.score)


class GradingBatch(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    things_to_grade = models.IntegerField()
    processed = models.IntegerField(default=0)  # this includes things that are graded, that errored during grading...


# Not used....
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
