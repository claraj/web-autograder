from django.db import models
from django.core.validators import RegexValidator
import logging
from datetime import datetime
import json
import re
log = logging.getLogger(__name__)


class ProgrammingClass(models.Model):
    name = models.CharField(max_length=100)  # e.g. Java Programming, Programming Logic...
    semester_code = models.CharField(max_length=6, null=False, blank=False, validators=[RegexValidator('^\d{6}$', message='Must be 6 numbers, year+semester code e.g. Fall 2019 is 201901')])  # summer = 201801, fall = 201803, spring 2019 = 201805
    semester_human_string = models.CharField(max_length=200, null=True, blank=True)

    semester_codes = { '01': 'Fall', '03': 'Spring', '05': 'Summer' }

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.semester_human_string, self.semester_code)

    def save(self, *args, **kwargs):
        class_instance.semester_human_string = humanCode(class_instance.semester_code)
        super(*args, **kwargs)


    def humanCode(self):
        """ Create human-readable versions (e.g. "Summer 2019") from semester codes like 201805 """

        try :
            yearStr = self.semester_code[0:4]
            code = self.semester_code[4:6]
            numYear = int(yearStr)
            semText = ProgrammingClass.semester_codes[semester]
            if semester_code in ['03', '05']:
                numYear += 1
            human_string = '%s %s' % (semText, numYear)
            self.semester_human_string = human_string
        except Exception as e:
            log.warning('Semester code %s could not be converted to human readable because %s' % (numberCode, e))



class Assignment(models.Model):
    # programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.PROTECT, blank=True, null=True)
    week = models.IntegerField()
    github_base = models.CharField(max_length=200)      # e.g. week-0-variables
    github_org = models.CharField(max_length=200)
    instructor_repo = models.CharField(max_length=200)  # eg. https://github.com/minneapolis-edu/JAG_0
    d2l_gradebook_url = models.CharField(max_length=200, blank=True, null=False)

    # class Meta:
    #     unique_together = ( ('week', 'programming_class'), )

    def __str__(self):
        return 'Class: [%s] Week: [%d] GitHub Base: [%s] Intructor Repo: [%s] D2L URL [%s] ' % (self.programming_class, self.week, self.github_base, self.instructor_repo, self.d2l_gradebook_url)


class Student(models.Model):
    # programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.PROTECT, null=True, blank=True)
    org_id = models.CharField(max_length=8, validators=[RegexValidator('^\d{8}$', message='MCTC Student ID must be 8 numbers')], null=False, blank=True)
    name = models.CharField(max_length=200, null=False, blank=False)   # Student real name, as used in D2L
    github_id = models.CharField(max_length=200, blank=True, null=False, validators=[RegexValidator('^[\S_-]+$', message='Only letters, numbers, underscores and hyphens.')] )
    star_id = models.CharField(max_length=8, validators=[RegexValidator('^[a-z]{2}\d{4}[a-z]{2}$', message='Star ID must be in the pattern ab1234cd')], null=False, blank=True)
    active = models.BooleanField(default=True)   # becomes False if student drops, withdraws, is abducted by aliens etc.

    def __str__(self):
        return 'Name: %s, GitHub ID: %s ' % (self.name, self.github_id)


class StudentProgrammingClass(models.Model):
    programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.PROTECT, null=False, blank=False)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, null=False, blank=False)


class AssignmentProgrammingClass(models.Model):
    programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.PROTECT, null=False, blank=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT, null=False, blank=False)


class GradeManager(models.Manager):
    def previous_grade_for_student_assignment(self, student, assignment):
        try:
            # Find most recent grade for this student's assignment
            latest = self.filter(student_id=student, assignment_id=assignment).order_by('-date')[:1][0]  # Limit 1, get first item
            return latest
        except IndexError as e:
            return None

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

    objects = GradeManager()


    def __str__(self):
        return 'assignment %s student %s batch %s date %s, score %f'  % (self.assignment.id, self.student.id, self.batch, self.date, self.score)


    def save(self, *args, **kwargs):

        self.generate_github_url()

        updating = self.id  # If no primary key, this Grade hasn't been saved before.

        if updating:
            # Save and return
            super().save(*args, **kwargs)
            return

        # if new Grade object creation, examine previous versions

        # does a previous version exist?
        previous_version = Grade.objects.previous_grade_for_student_assignment(self.student.id, self.assignment.id)

        if not previous_version:
            super().save(*args, **kwargs)
            return

        # If there is a previous version, check if same commit, look for previous comments

        # Is same commit? No code changes. Update batch of previous version to this batch and save. Do not save new Grade.
        if self.is_same_commit(previous_version):
            self.update_previous_grade_to_this_batch(previous_version)
            return

        # Different commit? Copy any previously saved comments from the last grade report to this report. Save.
        self.bring_comments_forward(previous_version)

        super().save(*args, **kwargs)


    def generate_github_url(self):
        if not self.assignment or not self.student:
            return
        url = 'https://github.com/%s/%s-%s' % ( self.assignment.github_org , self.assignment.github_base , self.student.github_id)
        self.student_github_url = url


    def is_same_commit(self, previous):
        return previous.github_commit_hash == self.github_commit_hash


    def update_previous_grade_to_this_batch(self, previous):
        previous.batch = self.batch
        previous.save()


    def get_timestring_prefix(self, date):
        return date.strftime('%m/%d/%y %H:%M ')   # 12/31/18 16:30


    def bring_comments_forward(self, previous):

        timestamp = self.get_timestring_prefix(previous.date)

        prev_rep = json.loads(previous.generated_report)
        new_rep = json.loads(self.generated_report)

        prev_questions = prev_rep['question_reports']
        new_questions = new_rep['question_reports']

        for (pq, nq) in zip(prev_questions, new_questions):
            if 'adjusted_points' in pq:
                nq['adjusted_points'] = pq['adjusted_points']
            if 'instructor_comments' in pq:
                comments = pq['instructor_comments']
                already_date = re.match(r'^\d\d/\d\d/\d\d', comments)
                if already_date:
                    nq['instructor_comments'] = pq['instructor_comments']
                else:
                    nq['instructor_comments'] = timestamp + pq['instructor_comments']

        if 'overall_instructor_comments' in prev_rep:

            comments = prev_rep['overall_instructor_comments']
            # does this start with a date?
            already_date = re.match(r'^\d\d/\d\d/\d\d', comments)
            if already_date:
                new_rep['overall_instructor_comments'] = prev_rep['overall_instructor_comments']
            else:
                new_rep['overall_instructor_comments'] = timestamp + prev_rep['overall_instructor_comments']

        self.generated_report = json.dumps(new_rep)



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
