from django.test import TestCase
from unittest.mock import Mock
from api.models import Grade, Student, Assignment, ProgrammingClass, GradingBatch
import json
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from api import grade_util
from dataclasses import dataclass
import re


TestCase.maxDiff = None

class TestGradeModel(TestCase):

    def setUp(self):
        self.asgt = Assignment.objects.create(week="1", github_base="base", github_org="org", instructor_repo="///")
        self.std = Student.objects.create(name="test", github_id="handle")
        self.pc = ProgrammingClass.objects.create(name="Reading the Manual", semester_code="202005")

        self.batch = GradingBatch.objects.create(id=str(uuid4()), things_to_grade=1)

    def test_generate_github_url(self):
        print(self.asgt, self.std)
        grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch="123e4567-e89b-12d3-a456-426655440000", score=0, github_commit_hash='abc123', programming_class=self.pc)
        expected = 'https://github.com/org/base-handle'
        grade.refresh_from_db()
        self.assertEqual(expected, grade.student_github_url)

    """
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


    def tests_grader_runs_saves_new_grade(self):
        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=uuid4(), generated_report='report', score=10, github_commit_hash='abc123', programming_class=self.pc, status=Grade.GRADED)
        self.assertEqual(1, Grade.objects.count())


    def tests_grader_runs_saves_new_student_error_grade(self):
        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=uuid4(), generated_report='report', score=0, github_commit_hash='abc123', programming_class=self.pc, status=Grade.STUDENT_ERROR)
        self.assertEqual(1, Grade.objects.count())


    def tests_grader_runs_saves_new_autograder_error_grade(self):
        new_grade = Grade.objects.create(assignment=self.asgt, ag_error="drat!", student=self.std, batch=uuid4(), programming_class=self.pc, status=Grade.AUTOGRADER_ERROR)
        self.assertEqual(1, Grade.objects.count())


    """ Tests for when there is a previous grade """


    def test_previous_grader_runs_this_student_errors(self):
        batch1, batch2 = uuid4(), uuid4()
        prev_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch1, generated_report='lots of info', score=10, github_commit_hash='abc123', programming_class=self.pc, status=Grade.GRADED)
        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch2, generated_report='errors', score=10, github_commit_hash='abc123', programming_class=self.pc, status=Grade.STUDENT_ERROR)
        self.assertEqual(new_grade.last_success, prev_grade.id)
        self.assertEqual(2, Grade.objects.count())


    def test_previous_grader_runs_this_autograder_errors(self):
        batch1, batch2 = uuid4(), uuid4()
        prev_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch1, generated_report='lots of info', score=10, github_commit_hash='abc123', programming_class=self.pc, status=Grade.GRADED)
        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch2, ag_error='Error!', programming_class=self.pc, status=Grade.AUTOGRADER_ERROR)
        self.assertEqual(new_grade.last_success, prev_grade.id)
        self.assertEqual(2, Grade.objects.count())


    def test_previous_grader_student_error_this_runs(self):
        batch1, batch2 = uuid4(), uuid4()
        prev_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch1, generated_report='errors', score=0, github_commit_hash='abc123', programming_class=self.pc, status=Grade.STUDENT_ERROR)
        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch2, generated_report='lots of info', score=10, github_commit_hash='def456', programming_class=self.pc, status=Grade.GRADED)
        self.assertEqual(2, Grade.objects.count())


    def test_previous_grader_student_error_this_errors_same_error(self):
        batch1, batch2 = uuid4(), uuid4()
        prev_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch1, generated_report='errors', score=0, github_commit_hash='abc123', programming_class=self.pc, status=Grade.STUDENT_ERROR)
        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch2, generated_report='errors', score=0, github_commit_hash='abc123', programming_class=self.pc, status=Grade.STUDENT_ERROR)
        self.assertEqual(1, Grade.objects.count())
        prev_grade.refresh_from_db()
        self.assertEqual(batch2, prev_grade.batch)


    def test_previous_grader_student_error_this_errors_different_error(self):
        batch1, batch2 = uuid4(), uuid4()
        prev_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch1, generated_report='errors', last_success=42, score=0, github_commit_hash='abc123', programming_class=self.pc, status=Grade.STUDENT_ERROR)
        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch2, generated_report='oops', score=0, github_commit_hash='def456', programming_class=self.pc, status=Grade.STUDENT_ERROR)
        self.assertEqual(2, Grade.objects.count())
        prev_grade.refresh_from_db()
        self.assertEqual(42, new_grade.last_success)


    def test_previous_grader_student_error_this_autograder_errors(self):
        batch1, batch2 = uuid4(), uuid4()
        prev_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch1, generated_report='errors', last_success=42, score=0, github_commit_hash='abc123', programming_class=self.pc, status=Grade.STUDENT_ERROR)
        new_grade = Grade.objects.create(assignment=self.asgt, ag_error="drat!", student=self.std, batch=batch2, programming_class=self.pc, status=Grade.AUTOGRADER_ERROR)
        self.assertEqual(2, Grade.objects.count())
        prev_grade.refresh_from_db()
        self.assertEqual(42, new_grade.last_success)


    def test_previous_grader_autograder_error_this_runs(self):
        batch1, batch2 = uuid4(), uuid4()
        prev_grade = Grade.objects.create(assignment=self.asgt, ag_error="drat!", student=self.std, batch=batch1, programming_class=self.pc, status=Grade.AUTOGRADER_ERROR)
        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch2, generated_report='lots of info', score=10, github_commit_hash='def456', programming_class=self.pc, status=Grade.GRADED)
        self.assertEqual(2, Grade.objects.count())


    def test_previous_grader_autograder_error_this_student_error(self):
        batch1, batch2 = uuid4(), uuid4()
        prev_grade = Grade.objects.create(assignment=self.asgt, ag_error="drat!", student=self.std, batch=batch1, last_success=42, programming_class=self.pc, status=Grade.AUTOGRADER_ERROR)
        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch1, generated_report='errors', score=0, github_commit_hash='abc123', programming_class=self.pc, status=Grade.STUDENT_ERROR)
        self.assertEqual(2, Grade.objects.count())
        self.assertEqual(42, new_grade.last_success)


    def test_previous_grader_autograder_error_this_autograder_error_same_error(self):
        batch1, batch2 = uuid4(), uuid4()
        prev_grade = Grade.objects.create(assignment=self.asgt, ag_error="drat!", student=self.std, batch=batch1, programming_class=self.pc, status=Grade.AUTOGRADER_ERROR)
        new_grade = Grade.objects.create(assignment=self.asgt, ag_error="drat!", student=self.std, batch=batch2, programming_class=self.pc, status=Grade.AUTOGRADER_ERROR)
        self.assertEqual(1, Grade.objects.count())
        prev_grade.refresh_from_db()
        self.assertEqual(batch2, prev_grade.batch)


    def test_previous_grader_autograder_error_this_autograder_error_different_error(self):
        batch1, batch2, batch3 = uuid4(), uuid4(), uuid4()
        prev_grade = Grade.objects.create(assignment=self.asgt, ag_error="drat!", student=self.std, batch=batch1, last_success=42, programming_class=self.pc, status=Grade.AUTOGRADER_ERROR)
        new_grade = Grade.objects.create(assignment=self.asgt, ag_error="oh no!", student=self.std, batch=batch2, programming_class=self.pc, status=Grade.AUTOGRADER_ERROR)

        self.assertEqual(2, Grade.objects.count())
        self.assertEqual(42, new_grade.last_success)

        another_new_grade = Grade.objects.create(assignment=self.asgt, ag_error="yikes", student=self.std, batch=batch3, programming_class=self.pc, status=Grade.AUTOGRADER_ERROR)
        self.assertEqual(3, Grade.objects.count())
        self.assertEqual(42, another_new_grade.last_success)


    """ Bunch of tests on bringing comments forward """

    def test_this_grader_runs_previous_grader_runs_updates_old_does_not_save_new_if_same_commit(self):
        old_batch = '11111111-aaaa-1111-aaaa-111111111111'
        new_batch = '55555555-eeee-5555-eeee-999999999999'

        old_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=old_batch, score=0, github_commit_hash='abc123', programming_class=self.pc)
        self.assertEqual(1, Grade.objects.count())

        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=new_batch, score=0, github_commit_hash='abc123', programming_class=self.pc)
        self.assertEqual(1, Grade.objects.count())

        old_grade.refresh_from_db()
        self.assertEqual(new_batch, str(old_grade.batch))

        self.assertFalse(Grade.objects.filter(id=new_grade.id).exists())  # new grade not saved


    def test_this_grader_runs_previous_grader_runs_brings_comments_forward_to_new_grade(self):
        datestr = '12/31/18 16:30 '
        date = datetime(2018, 12, 31, hour=16, minute=30, tzinfo=timezone(timedelta(0)))

        batch_1 = 'b1111111-0000-0000-0000-000000000000'
        batch_2 = 'b2222222-0000-0000-0000-000000000000'

        old_comments = { 'question_reports': [
            {'adjusted_points': 2, 'instructor_comments': 'woweeee'},
            {'adjusted_points': 10, 'instructor_comments': 'meh'}
        ]}

        new_generated_comments = { 'question_reports': [ {'whatever': 123}, {'something': 'stuff'} ]}

        updated_new_generated_comments = { 'question_reports': [
            {'whatever': 123, 'adjusted_points': 2, 'instructor_comments': datestr + 'woweeee'},
            {'something': 'stuff', 'adjusted_points': 10, 'instructor_comments': datestr + 'meh'} ]}

        # Existing grade has comments and adjusted points. Comments should be timestamped and bought forward, adjusted points bought forward
        old_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_1, score=12, github_commit_hash='something', generated_report=json.dumps(old_comments), programming_class=self.pc)
        old_grade.date = date
        old_grade.save()

        old_grade.refresh_from_db()

        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_2, score=12, github_commit_hash='different', generated_report=json.dumps(new_generated_comments), programming_class=self.pc)

        new_grade.refresh_from_db()

        self.assertDictEqual(updated_new_generated_comments, json.loads(new_grade.generated_report))


    def test_unmodified_brought_forward_comments_new_grading_batch_same_commit_preserves_in_old_grade(self):
        # new grading batch, if commit is the same, then the comments from the previous are preserved

        old_batch = '11111111-aaaa-1111-aaaa-111111111111'
        new_batch = '55555555-eeee-5555-eeee-999999999999'

        old_gen_report = { 'question_reports': [ {'adjusted_points': 2, 'instructor_comments': 'woweeee'}, {'adjusted_points': 10, 'instructor_comments': 'meh'} ]}
        new_gen_report = {}

        old_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=old_batch, generated_report=json.dumps(old_gen_report), score=0, github_commit_hash='abc123', programming_class=self.pc)

        # same commit
        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=new_batch, generated_report=json.dumps(new_gen_report), score=0, github_commit_hash='abc123', programming_class=self.pc)
        self.assertEqual(1, Grade.objects.count())

        old_grade.refresh_from_db()

        self.assertEqual(new_batch, str(old_grade.batch))
        self.assertFalse(Grade.objects.filter(id=new_grade.id).exists())  # new grade not saved
        self.assertDictEqual(old_gen_report, json.loads(old_grade.generated_report))  # and report is the same.


    def test_unmodified_brought_forward_comments_new_grading_batch_different_commit_preserves_in_new_grade(self):
        # no new date added to a comment like '12/31/2018 4.30 some comments when brought forward'

        # datestr_1 = '11/04/18 11.30am '
        # date_1= datetime(2018, 11, 4, hour=11, minute=30)

        datestr = '12/31/18 16:30 '
        date = datetime(2018, 12, 31, hour=16, minute=30)

        # mock_timestring = Mock(return_value=datestr)  # but should not be used.
        # Grade.get_timestring_prefix = mock_timestring

        batch_1 = 'b1111111-0000-0000-0000-000000000000'
        batch_2 = 'b2222222-0000-0000-0000-000000000000'
        batch_3 = 'b3333333-0000-0000-0000-000000000000'

        # Assumes a previous batch ran, and the report is as follows.
        dated_generated_report = { 'question_reports': [
            {'question': '1', 'adjusted_points': 2, 'instructor_comments': datestr + 'woweeee'},
            {'question': '2', 'adjusted_points': 10, 'instructor_comments': datestr + 'meh'}
        ]}

        first_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_1, score=12, github_commit_hash='something', generated_report=json.dumps(dated_generated_report), date=date, programming_class=self.pc)

        # Run another batch. Comments should be brought forward into new Grade with no modifications.
        before_comments_report = { 'question_reports':
        [
            {'question': '1'},
            {'question': '2'}
        ]}

        second_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_2, score=12, github_commit_hash='different', generated_report=json.dumps(before_comments_report), programming_class=self.pc)

        second_grade.refresh_from_db()

        self.assertDictEqual(dated_generated_report, json.loads(second_grade.generated_report))  # Not modified


    def test_brought_forward_comments_modified_new_grading_batch_different_commit_preserves_in_new_grade_new_date_added(self):
        # comments like 'and another thing.... 12/31/2018 4.30 some comments' are bought forward with new timestring from last batch
        # as "1/03/2019 11.40am and another thing.... 12/31/2018 4.30 some comments"

        datestr_1 = '11/04/18 11:30 '
        date_1= datetime(2018, 11, 4, hour=11, minute=30)

        datestr_2 = '12/31/18 16:13 '
        date_2 = datetime(2018, 12, 31, hour=16, minute=13, tzinfo=timezone(timedelta(0)))

        # mock_timestring = Mock(side_effect=[datestr_1, datestr_2])
        # Grade.get_timestring_prefix = mock_timestring

        batch_1 = 'b1111111-0000-0000-0000-000000000000'
        batch_2 = 'b2222222-0000-0000-0000-000000000000'

        # Assumes a previous batch ran, and the report is as follows, and the user has made some edits.
        dated_generated_report = { 'question_reports': [
            {'question': '1', 'adjusted_points': 2, 'instructor_comments': 'And another thing! ' + datestr_1 + 'woweeee'},
            {'question': '2', 'adjusted_points': 10, 'instructor_comments': 'Something else...' + datestr_1 + 'meh'} ]
        }

        first_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_1, score=12, github_commit_hash='something', generated_report=json.dumps(dated_generated_report), programming_class=self.pc)
        first_grade.date = date_2
        first_grade.save()
        first_grade.refresh_from_db()


        # Run another batch. Comments should be brought forward into new Grade, prefixed by timestamp.
        before_comments_report = { 'question_reports':     [
                {'question': '1'},
                {'question': '2'}
            ]}

        second_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_2, score=12, github_commit_hash='different', generated_report=json.dumps(before_comments_report), programming_class=self.pc)

        second_grade.refresh_from_db()

        expected_second_dated_report = { 'question_reports': [
            {'question': '1', 'adjusted_points': 2, 'instructor_comments': datestr_2 + 'And another thing! ' + datestr_1 + 'woweeee'},
            {'question': '2', 'adjusted_points': 10, 'instructor_comments': datestr_2 + 'Something else...' + datestr_1 + 'meh'} ]
        }

        self.assertDictEqual(expected_second_dated_report, json.loads(second_grade.generated_report))  # Not modified
