# mock queue_grading_task for now, replace with celery or huey or djangoq

import time
import random
from threading import Thread
from api.models import Student, Assignment, Grade

from django_q.tasks import async_task, result


def queue_grading_task(batch, assignment_id, student_id):
    task_id = async_task(invoke_grader, batch, assignment_id, student_id, hook=save_result)
    print(f'the task id is {task_id}')

def invoke_grader(b, a, s):

    # TODO actually grade thing
    timer = random.randint(2, 4)
    print(f'this will take {timer} seconds. thing to grade: {b} assignment {a} student {s}')
    time.sleep(random.randint(2, 4))
    grade = random.choice([3.2, 7.4, 9.0, 10.12])
    report = random.choice(['eh', 'huh', 'wow!!!!', 'meh'])

    return {
        'batch': b,
        'assignment_id': a,
        'student_id':s,
        'score': grade,
        'generated_report': report
    }


def save_result(task):
    print(f'this task result is {task.result}')
    result = task.result

    grade = Grade(**result)
    # grade = Grade(student=student, assignment=assignment, batch=batch, score=result)
    grade.save()




# def queue_grading_task(batch, assignment_id, student_id):
#
#     class MockGrade(Thread):
#         def run(self):
#             # TODO handle errors here .
#             time.sleep(random.randint(2, 12))
#             student = Student.objects.get(pk=student_id)
#             assignment = Assignment.objects.get(pk=assignment_id)
#             grade = Grade(student=student, assignment=assignment, batch=batch, score=random.choice( [1.23, 3.45, 6.78, 9.01]) )
#             print('mock grade to save:::', grade)
#             try:
#                 grade.save()
#             except:
#                 print('error saving')
#     mock_grade = MockGrade().start()
