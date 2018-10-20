from api.models import Student, Assignment, Grade
from grading_module import ag

from django_q.tasks import async_task, result

def queue_grading_task(batch, assignment_id, student_id):
    print(f'hello from queue launcher! batch {batch}')
    task_id = async_task(start_grader, batch, assignment_id, student_id, hook=save_result)


def start_grader(batch, assignment_id, student_id):

    print('INVOKE GRADER GO hello this is real grader')

    student = Student.objects.get(pk=student_id)
    assignment = Assignment.objects.get(pk=assignment_id)
    report, score = ag.grade(assignment, student)

    return {
        'batch': batch,
        'assignment_id': assignment_id,
        'student_id': student_id,
        'score': score,
        'generated_report': str(report)  # TODO
    }



def save_result(task):
    if task.success:
        result = task.result
        print(f'HELLO FROM HOOK this task result is {task.result}')
        grade = Grade(**result)
        grade.save()
    else:
        # get error message and report in some way.
        print('oops, ', task.error)
