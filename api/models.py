from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime
import json
import re
import logging
logger = logging.getLogger(__name__)

from . import grade_util


class ProgrammingClass(models.Model):
    name = models.CharField(max_length=100)  # e.g. Java Programming, Programming Logic...
    semester_code = models.CharField(max_length=6, null=False, blank=False, validators=[RegexValidator('^20\d{2}0[135]$', message='Must be 6 numbers, year+semester code e.g. Fall 2019 is 201901')])  # summer = 201801, fall = 201803, spring 2019 = 201805
    semester_human_string = models.CharField(max_length=200, null=True, blank=True)

    semester_codes = { '01': 'Fall', '03': 'Spring', '05': 'Summer' }

    def __str__(self):
        return f'{self.name}, {self.semester_human_string}, {self.semester_code}'


    def save(self, *args, **kwargs):
        self.semester_human_string = self.humanCode()
        super().save(*args, **kwargs)


    def humanCode(self):
        """ Create human-readable versions (e.g. "Summer 2019") from semester codes like 201805 """

        try :
            year_str = self.semester_code[0:4]  # e.g. '2018'
            semester_code_str = self.semester_code[4:6]
            semester_text = ProgrammingClass.semester_codes[semester_code_str]  # 'Fall', 'Spring', 'Summer'

            numerical_year = int(year_str)   # 01, 03, 05
            if semester_code_str in ['03', '05']:
                numerical_year += 1
            human_string = f'{semester_text}, {numerical_year}'
            return human_string

        except Exception as e:
            logger.warning(f'Can\'s create human-readable string for semester code {self.semester_code} because {e}')



class Assignment(models.Model):
    programming_classes = models.ManyToManyField(ProgrammingClass, blank=True)
    week = models.IntegerField()
    github_base = models.CharField(max_length=200)      # e.g. week-0-variables
    github_org = models.CharField(max_length=200)
    instructor_repo = models.CharField(max_length=200)  # e.g. https://github.com/minneapolis-edu/JAG_0
    d2l_gradebook_url = models.CharField(max_length=200, blank=True, null=False)

    def __str__(self):
        return f'Week: {self.week} GitHub Base: {self.github_base}, org: {self.github_org}, Intructor Repo: {self.instructor_repo} D2L URL {self.d2l_gradebook_url}'


class Student(models.Model):
    programming_classes = models.ManyToManyField(ProgrammingClass)
    org_id = models.CharField(max_length=8, validators=[RegexValidator('^\d{8}$', message='MCTC Student ID must be 8 numbers')], null=False, blank=True)
    name = models.CharField(max_length=200, null=False, blank=False)   # Student real name, as used in D2L
    github_id = models.CharField(max_length=200, blank=True, null=False, validators=[RegexValidator('^[\S_-]+$', message='Only letters, numbers, underscores and hyphens.')] )
    star_id = models.CharField(max_length=8, validators=[RegexValidator('^[a-z]{2}\d{4}[a-z]{2}$', message='Star ID must be in the pattern ab1234cd')], null=False, blank=True)
    active = models.BooleanField(default=True)   # becomes False if student drops, withdraws, is abducted by aliens etc.

    def __str__(self):
        return f'Name: {self.name}, GitHub ID: {self.github_id}, StarID {self.star_id}'


class GradeManager(models.Manager):
    def previous_grade_for_student_assignment(self, student, assignment):
        try:
            # Find most recent grade for this student's assignment
            latest = self.filter(student_id=student, assignment_id=assignment).order_by('-date')[:1][0]  # Limit 1, get first item
            return latest
        except IndexError as e:
            return None


class Grade(models.Model):
    # for an assignment and student and programming class. The assignment knows what programming class it belongs to.

    GRADED = 'GR'
    STUDENT_ERROR = "SE"
    AUTOGRADER_ERROR = "AE"

    STATUS_CHOICES = (
        (GRADED, 'Succesfully graded'),
        (STUDENT_ERROR, 'Error in student code or code not found'),
        (AUTOGRADER_ERROR, 'Autograder errored')
    )

    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT, blank=False, null=False)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, blank=False, null=False)
    programming_class = models.ForeignKey(ProgrammingClass, blank=False, null=False, on_delete=models.PROTECT)
    generated_report = models.TextField(blank=True, null=True)
    instructor_comments = models.TextField(blank=True, null=True)
    score = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    student_github_url = models.CharField(max_length=400, blank=True)
    batch = models.UUIDField()
    github_commit_hash = models.CharField(max_length=40, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True)
    ag_error = models.TextField(blank=True, null=True)  # errors from grading process, could be programatic errors
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=GRADED)
    last_success = models.IntegerField(default=-1)   # If this Grade represents an error, this field contains the last grade for this student/assignment/class combo that did run correctly, if there was one.

    objects = GradeManager()

    def __str__(self):
        return f'{self.id} assignment {self.assignment.id} student {self.student.id} batch {self.batch} date {self.date}, score {self.score}'


    def save(self, *args, **kwargs):

        print('SAVING')
        self.student_github_url = grade_util.generate_github_url(self)
        print('github', self.student_github_url)

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

        # If there is a previous version, check if same commit, and same error. look for previous comments

        """ Three scenarios:
            1. Grader runs, produces test reports and score. commit_hash set.
                 -- This run may be different or same commit hash.
            2. student error: Grader attempts to run, student's code crashes or errors. commit_hash may (code didn't compile) or may not be set (not found). generated_report has error attribute. e.g. "{"error": "no code", "reason": "not found"}". Grade does not have ag_error attribute set.
                 -- May have same or different commit hash.
            3. my error: My code crashes, the instructor repo has vanished... my problem. generated_report is empty and ag_error is set.

            Before the new grade was creatd, the previous grade could be in one of four states. So there are many combinations of previous and new.


            1. PREVIOUS: Grader Runs. May Have Instructor Comments
                  NEW: Grader Runs. Same commit hash                --> Change date and batch of previous to new, don't save new
                  NEW: Grader Runs. Different commit hash           --> Save new Grade and bring instructor comments forward
                  NEW: Student Error. commit hash is different      --> Save new Grade, set last_success to previous.id
                  NEW: Student Error. commit is the same as before  --> Save new Grade, set last_success to previous.id
                  NEW: My Error                                     --> Save new Grade, set last_success to previous.id

            2. PREVIOUS: Student Error with commit hash (code exists, errors running)
                  NEW: Grader Runs. Same commit hash                --> Save new Grade
                  NEW: Grader Runs. Different commit hash           --> Save new Grade
                  NEW: Student Error. commit hash is different      --> Save new Grade, set last_success to previous.last_success if present
                  NEW: Student Error. commit is the same as before  --> Save new Grade, set last_success to previous.last_success if present
                  NEW: My Error                                     --> Save new Grade, set last_success to previous.last_success if present

            3. PREVIOUS: Student Error with no commit hash (e.g code not found)
                  NEW: Grader Runs. New commit hash                 --> Save new Grade
                  NEW: Student Error with commit hash               --> Save new Grade, set last_success to previous.id if present
                  NEW: Student Error with no commit hash            --> Change date and batch of previous to new, don't save
                  NEW: My Error                                     --> Save new Grade, set last_success to previous.id if present

            4. PREVIOUS: My Error (no commit hash will be saved)
                  NEW: Grader Runs                                  --> Save new Grade
                  NEW: Student Error. commit hash or no commit hash --> Save new Grade, set last_success to previous.last_success if present
                  NEW: My Error - same                              --> Change date and batch of previous to new, don't save
                  NEW: My Error - different error                   --> Save new Grade, set last_success to previous.last_success if present

        """


        if previous_version.status == Grade.GRADED:
            if self.status == Grade.GRADED:
                if grade_util.is_same_commit(self, previous_version):
                    previous_version.batch = self.batch
                    previous_version.save()
                    return
                else:
                    self.generated_report = grade_util.bring_comments_forward(self, previous_version)
                    super().save(*args, **kwargs)
                    return

            if self.status == Grade.STUDENT_ERROR or self.status == Grade.AUTOGRADER_ERROR:
                self.last_success = previous_version.id
                super().save(*args, **kwargs)
                return


        if previous_version.status == Grade.STUDENT_ERROR:
            if self.status == Grade.GRADED:
                super().save(*args, **kwargs)
                return

            if self.status == Grade.STUDENT_ERROR:
                if self.generated_report == previous_version.generated_report:
                    self.update_previous_grade_to_this_batch(previous_version)
                    return
                else:
                    self.last_success = previous_version.last_success
                    super().save(*args, **kwargs)
                    return

            if self.status == Grade.AUTOGRADER_ERROR:
                self.last_success = previous_version.last_success
                super().save(*args, **kwargs)
                return


        if previous_version.status == Grade.AUTOGRADER_ERROR:
            if self.status == Grade.GRADED:
                super().save(*args, **kwargs)
                return
            if self.status == Grade.STUDENT_ERROR:
                self.last_success = previous_version.last_success
                super().save(*args, **kwargs)
                return
            if self.status == Grade.AUTOGRADER_ERROR:
                if self.ag_error == previous_version.ag_error:
                    self.update_previous_grade_to_this_batch(previous_version)
                    return
                else:
                    self.last_success = previous_version.last_success
                    super().save(*args, **kwargs)
                    return


    def update_previous_grade_to_this_batch(self, previous):
        previous.batch = self.batch
        previous.save()


class GradingBatch(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    things_to_grade = models.IntegerField()
    processed = models.IntegerField(default=0)  # this includes things that are graded, that errored during grading...
