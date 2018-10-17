# mock queue_grading_task for now, replace with celery or huey or djangoq

import time
import random
from threading import Thread
from api.models import Student, Assignment, Grade

from django_q.tasks import async_task, result


def queue_grading_task(batch, assignment_id, student_id):
    task_id = async_task(invoke_grader, batch, assignment_id, student_id, hook=save_result)
    print(f'the task id is {task_id}')

def invoke_grader(batch, assignment, student):

    # TODO actually grade thing
    timer = random.randint(2, 4)
    print(f'this will take {timer} seconds. thing to grade: {batch} assignment {assignment} student {student}')
    time.sleep(random.randint(2, 4))
    grade = random.choice([3.2, 7.4, 9.0, 10.12])
    report = random.choice(['eh', 'huh', 'wow!!!!', 'meh'])

    print('USE GRADER MODULE TO GRADE THING')


    return {
        'batch': batch,
        'assignment_id': assignment,
        'student_id': student,
        'score': grade,
        'generated_report': report
    }


def save_result(task):
    print(f'this task result is {task.result}')
    result = task.result
    grade = Grade(**result)
    grade.save()
