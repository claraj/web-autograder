from django.test import TestCase
from unittest.mock import Mock
from api.models import Grade, Student, Assignment
import json
from datetime import datetime, timezone, timedelta


TestCase.maxDiff = None

class TestGradeModel(TestCase):


    def setUp(self):
        self.asgt = Assignment.objects.create(week="1", github_base="base", github_org="org", instructor_repo="///")
        self.std = Student.objects.create(name="test", github_id="handle")


    def test_generate_github_url(self):
        grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch="123e4567-e89b-12d3-a456-426655440000", score=0, github_commit_hash='abc123')
        expected = 'https://github.com/org/base-handle'
        grade.refresh_from_db()
        self.assertEqual(expected, grade.student_github_url)


    def test_updates_old_does_not_save_new_if_same_commit(self):
        old_batch = '11111111-aaaa-1111-aaaa-111111111111'
        new_batch = '55555555-eeee-5555-eeee-999999999999'

        old_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=old_batch, score=0, github_commit_hash='abc123')
        self.assertEqual(1, Grade.objects.count())

        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=new_batch, score=0, github_commit_hash='abc123')
        self.assertEqual(1, Grade.objects.count())

        old_grade.refresh_from_db()
        self.assertEqual(new_batch, str(old_grade.batch))

        self.assertFalse(Grade.objects.filter(id=new_grade.id).exists())  # new grade not saved


    def test_brings_comments_forward(self):

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
        old_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_1, score=12, github_commit_hash='something', generated_report=json.dumps(old_comments))
        old_grade.date = date
        old_grade.save()

        old_grade.refresh_from_db()
        print('DATE', old_grade.date)

        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_2, score=12, github_commit_hash='different', generated_report=json.dumps(new_generated_comments))

        new_grade.refresh_from_db()

        self.assertDictEqual(updated_new_generated_comments, json.loads(new_grade.generated_report))


    def test_unmodified_brought_forward_comments_new_grading_batch_same_commit_preserves_in_old_grade(self):
        # new grading batch, if commit is the same, then the comments from the previous are preserved

        old_batch = '11111111-aaaa-1111-aaaa-111111111111'
        new_batch = '55555555-eeee-5555-eeee-999999999999'

        old_gen_report = { 'question_reports': [ {'adjusted_points': 2, 'instructor_comments': 'woweeee'}, {'adjusted_points': 10, 'instructor_comments': 'meh'} ]}
        new_gen_report = {}

        old_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=old_batch, generated_report=json.dumps(old_gen_report), score=0, github_commit_hash='abc123')

        # same commit
        new_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=new_batch, generated_report=json.dumps(new_gen_report), score=0, github_commit_hash='abc123')
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

            first_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_1, score=12, github_commit_hash='something', generated_report=json.dumps(dated_generated_report), date=date)

            # Run another batch. Comments should be brought forward into new Grade with no modifications.
            before_comments_report = { 'question_reports':
            [
                {'question': '1'},
                {'question': '2'}
            ]}

            second_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_2, score=12, github_commit_hash='different', generated_report=json.dumps(before_comments_report))

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

            first_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_1, score=12, github_commit_hash='something', generated_report=json.dumps(dated_generated_report))
            first_grade.date = date_2
            first_grade.save()
            first_grade.refresh_from_db()


            # Run another batch. Comments should be brought forward into new Grade, prefixed by timestamp.
            before_comments_report = { 'question_reports':     [
                    {'question': '1'},
                    {'question': '2'}
                ]}

            second_grade = Grade.objects.create(assignment=self.asgt, student=self.std, batch=batch_2, score=12, github_commit_hash='different', generated_report=json.dumps(before_comments_report))

            second_grade.refresh_from_db()

            expected_second_dated_report = { 'question_reports': [
                {'question': '1', 'adjusted_points': 2, 'instructor_comments': datestr_2 + 'And another thing! ' + datestr_1 + 'woweeee'},
                {'question': '2', 'adjusted_points': 10, 'instructor_comments': datestr_2 + 'Something else...' + datestr_1 + 'meh'} ]
            }

            print('SECOND REP', expected_second_dated_report)
            print('IN DB', second_grade.generated_report)

            self.assertDictEqual(expected_second_dated_report, json.loads(second_grade.generated_report))  # Not modified
