from django.test import TestCase
from unittest.mock import MagicMock, patch
from api.models import Grade, Student, Assignment, ProgrammingClass, GradingBatch
from grading_module import ag
from django.forms.models import model_to_dict
from django_q.tasks import result
from uuid import UUID
import json
from decimal import Decimal


from autograder import grading_queue

TestCase.maxDiff = None


class TestQueue(TestCase):

    def setUp(self):
        self.batch_uuid = UUID('{12345678-1234-5678-1234-567812345678}')
        self.std = Student.objects.create(name="cat")
        self.asgt = Assignment.objects.create(github_base="base", github_org="org", week=1, instructor_repo="http://a.b.com")
        self.pc = ProgrammingClass.objects.create(name="learn code", semester_code="201905")
        self.batch = GradingBatch.objects.create(id=self.batch_uuid, things_to_grade=1)

    def test_success(self):

        with patch('grading_module.ag.grade', return_value={'success': True, 'report': 'blah blah', 'sha': 'abc123', 'score': 12}) as patched_ag:

            batch = self.batch.id

            task_id = grading_queue.queue_grading_task(batch, self.asgt.id, self.std.id, self.pc.id, testing=True)  #asgt 1, student 1, class 1
            # wait...
            task_result = result(task_id, 2000)

            # Hook should have saved Grade
            grade = Grade.objects.get(batch=batch)
            grade_dict = model_to_dict(grade)
            grade_dict.pop('student_github_url')
            grade_dict.pop('id')
        
            expected_grade = {
                    'ag_error': None,
                    'batch': batch,
                    'assignment': self.asgt.id,
                    'student': self.std.id,
                    'programming_class': self.pc.id,
                    'score': Decimal(12),
                    'generated_report': 'blah blah',
                    'github_commit_hash': 'abc123',
                    'instructor_comments': None
                    }

            self.assertDictEqual(expected_grade, grade_dict)
            self.batch.refresh_from_db()
            self.assertEqual(1, self.batch.processed)


    def test_error_running_student_code(self):

        with patch('grading_module.ag.grade', return_value={'success': True, 'report': 'errors and errors', 'sha': 'abc123', 'score': 0}) as patched_ag:

            batch = self.batch.id
            task_id = grading_queue.queue_grading_task(batch, self.asgt.id, self.std.id, self.pc.id, testing=True)  #asgt 1, student 1, class 1
            # wait...
            task_result = result(task_id, 2000)

            # Hook should have saved Grade
            grade = Grade.objects.get(batch=batch)
            grade_dict = model_to_dict(grade)
            grade_dict.pop('student_github_url')
            grade_dict.pop('id')

            expected_grade = {
                    'ag_error': None,
                    'batch': batch,
                    'assignment': self.asgt.id,
                    'student': self.std.id,
                    'programming_class': self.pc.id,
                    'score': Decimal(0),
                    'generated_report': 'errors and errors',
                    'github_commit_hash': 'abc123',
                    'instructor_comments': None
                    }

            self.assertDictEqual(expected_grade, grade_dict)
            self.batch.refresh_from_db()
            self.assertEqual(1, self.batch.processed)


    def test_error_fetching_student_code(self):

        with patch('grading_module.ag.grade', return_value={'success': True, 'report': 'errors and errors', 'sha': None, 'score': 0}) as patched_ag:
            batch = self.batch.id
            task_id = grading_queue.queue_grading_task(batch, self.asgt.id, self.std.id, self.pc.id, testing=True)  #asgt 1, student 1, class 1
            # wait...
            task_result = result(task_id, 2000)

            # Hook should have saved Grade
            grade = Grade.objects.get(batch=batch)
            grade_dict = model_to_dict(grade)
            grade_dict.pop('student_github_url')
            grade_dict.pop('id')

            expected_grade = {
                    'ag_error': None,
                    'batch': batch,
                    'assignment': self.asgt.id,
                    'student': self.std.id,
                    'programming_class': self.pc.id,
                    'score': Decimal(0),
                    'generated_report': 'errors and errors',
                    'github_commit_hash': None,
                    'instructor_comments': None
                    }

            self.assertDictEqual(expected_grade, grade_dict)
            self.batch.refresh_from_db()
            self.assertEqual(1, self.batch.processed)


    def test_exception_running_code(self):

        with patch('grading_module.ag.grade', return_value={'success': False, 'error': 'you have errored'}) as patched_ag:
            batch = self.batch.id
            task_id = grading_queue.queue_grading_task(batch, self.asgt.id, self.std.id, self.pc.id, testing=True)  #asgt 1, student 1, class 1
            # wait...
            task_result = result(task_id, 2000)

            # Hook should have saved Grade
            grade = Grade.objects.get(batch=batch)
            grade_dict = model_to_dict(grade)
            grade_dict.pop('student_github_url')
            grade_dict.pop('id')

            expected_grade = {
                    'ag_error': 'you have errored',
                    'batch': batch,
                    'assignment': self.asgt.id,
                    'student': self.std.id,
                    'programming_class': self.pc.id,
                    'score': Decimal(0),
                    'generated_report': None,
                    'github_commit_hash': None,
                    'instructor_comments': None
                    }

            self.assertDictEqual(expected_grade, grade_dict)
            self.batch.refresh_from_db()
            self.assertEqual(1, self.batch.processed)


    def test_unhandled_exception_running_code(self):

        with patch('grading_module.ag.grade', side_effect=Exception('Drat!')) as patched_ag:
            batch = self.batch.id

            task_id = grading_queue.queue_grading_task(batch, self.asgt.id, self.std.id, self.pc.id, testing=True)  #asgt 1, student 1, class 1
            # wait...
            task_result = result(task_id, 2000)

            # Hook should have saved Grade
            grade = Grade.objects.get(batch=batch)
            grade_dict = model_to_dict(grade)
            grade_dict.pop('student_github_url')
            grade_dict.pop('id')

            expected_grade = {
                    'ag_error': 'Drat!',
                    'batch': batch,
                    'assignment': self.asgt.id,
                    'student': self.std.id,
                    'programming_class': self.pc.id,
                    'score': Decimal(0),
                    'generated_report': None,
                    'github_commit_hash': None,
                    'instructor_comments': None
                    }

            self.assertDictEqual(expected_grade, grade_dict)
            self.batch.refresh_from_db()
            self.assertEqual(1, self.batch.processed)
