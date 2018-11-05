from api.models import Student, Assignment, Grade, GradingBatch, ProgrammingClass
from grading_module import ag
from django.db.models import F
import json
from datetime import datetime
import re
import logging
logger = logging.getLogger(__name__)

from django_q.tasks import async_task, result


def queue_grading_task(batch, assignment_id, student_id, class_id, testing=False):
    logger.info(f'hello from queue launcher! batch {batch}')

    student = Student.objects.get(pk=student_id)
    assignment = Assignment.objects.get(pk=assignment_id)
    programming_class = ProgrammingClass.objects.get(pk=class_id)

    task_id = async_task(start_grader, batch, assignment, student, programming_class, hook=save_result, sync=testing)
    return task_id


def start_grader(batch, assignment, student, programming_class):

    """
    Adds a grading task to the queue.
    Arguments: batch as UUID, and assignments, student, and programming_class objects.

    Types of outcomes:
        - The grader errors (probably my fault)
            The grader returns { success: False, error: 'error message' }
        - The grader attempts to grade but repo not found, code won't compile - student's fault
            Code found but error running: The grader returns { success: True, report: "{'error': 'not work', 'reason': 'because'}" , score: 0, sha: the_sha }
            Can't get code from GitHub: The grader returns { success: True, report: "{'error': 'not work', 'reason': 'because'}", score: 0, sha: None }
        - The grader grades
            The grader returns { success: True, report: "{ ...bunch of reports}", score: 99, sha: the_sha}

    """

    logger.info(f'Will launch grader for {student}, {assignment}')

    try:
        result = ag.grade(assignment, student)
        logger.info(f'grader results for {student.id} {assignment.id} are {result}')

        print('RESULT',result)
        if result['success']:

            # student error, or ran correctly?
            status = Grade.GRADED 
            if 'error' in json.loads(result['report']):
                status = Grade.STUDENT_ERROR

            return {
                'ag_error': None,
                'batch': batch,
                'assignment_id': assignment.id,
                'student_id': student.id,
                'programming_class_id': programming_class.id,
                'score': result['score'],
                'generated_report': result['report'],
                'github_commit_hash': result['sha'],
                'status': status
                }

        else:
            return {
                'ag_error': result['error'],
                'batch': batch,
                'assignment_id': assignment.id,
                'student_id': student.id,
                'programming_class_id': programming_class.id,
                'score': 0,
                'status': Grade.AUTOGRADER_ERROR
            }

    except Exception as e:
        # These are programatic errors - like the docker config is wrong or some other coding error
        # Probably my problem

        return {
            'ag_error': str(e),
            'batch': batch,
            'assignment_id': assignment.id,
            'student_id': student.id,
            'programming_class_id': programming_class.id,
            'score': 0
        }


def save_result(task):

    logger.info(f'Save hook, task {task}')
    try:
        if task.success:
            result = task.result
            logger.info(f'HOOK this task result is {result}')
            grade = Grade.objects.create(**result)

        else:
            logger.error(f'HOOK task was not succesful {task.result}')

    except Exception as e:
        logger.exception(f'HOOK Error saving grader result because {e}')

    # Whatever the outcome, increment number of things processed in this batch
    batch = GradingBatch.objects.get(id=result['batch'])
    batch.processed = F('processed') + 1  #https://docs.djangoproject.com/en/2.1/ref/models/expressions/
    batch.save()
