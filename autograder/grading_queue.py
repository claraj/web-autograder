# mock queue_grading_task for now, replace with celery or huey or djangoq

import time
import random
from threading import Thread
from api.models import Student, Assignment, Grade

def queue_grading_task(batch, assignment_id, student_id):


    class MockGrade(Thread):
        def run(self):
            time.sleep(random.choice([2, 4, 6, 8, 10, 12]))
            student = Student.objects.get(pk=student_id)
            assignment = Assignment.objects.get(pk=assignment_id)
            grade = Grade(student=student, assignment=assignment, batch=batch, score=random.choice( [1.23, 3.45, 6.78, 9.01]) )
            print('mock grade to save:::', grade)
            try:
                grade.save()
            except:
                print('error saving')
    mock_grade = MockGrade().start()
