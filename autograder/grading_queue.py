from api.models import Student, Assignment, Grade, GradingBatch
from grading_module import ag
from django.db.models import F

from django_q.tasks import async_task, result


def queue_grading_task(batch, assignment_id, student_id):
    print(f'hello from queue launcher! batch {batch}')
    task_id = async_task(start_grader, batch, assignment_id, student_id, hook=save_result)


def start_grader(batch, assignment_id, student_id):

    print('INVOKE GRADER GO hello this is real grader')

    student = Student.objects.get(pk=student_id)
    assignment = Assignment.objects.get(pk=assignment_id)
    result = ag.grade(assignment, student)

    if 'error' in result:
        # These are programatic errors - like the docker config is wrong or some other coding error
        # Probably my problem
        print('ERROR grading:', result['error'] )
        err = result['error']
        return {
            'error': result['error'],
            'batch': batch,
            'assignment_id': assignment_id,
            'student_id': student_id,
            'score': 0,
            'generated_report': f'Error running grader because {err}'  # TODO format?
        }

    # Errors like - code doesn't compile, repo not found... save in the Grade object anyway so client

    report, score = result['result']

    return {
        'error': None,
        'batch': batch,
        'assignment_id': assignment_id,
        'student_id': student_id,
        'score': score,
        'generated_report': report  # TODO format?
    }



def save_result(task):

    if task.success:

        result = task.result

        if result:
            print(f'HELLO FROM HOOK this task result is {result}')
            grade = Grade(**result)
            grade.save()


        else:
            # get error message and report in some way.
            print('THIS IS HOOK there was error, ', result['error'])

    else:
        print('THIS IS HOOK task was not succesful')


    # And increment number of things processed in this batch
    batch = GradingBatch.objects.get(id=result['batch'])
    batch.processed = F('processed') + 1  #https://docs.djangoproject.com/en/2.1/ref/models/expressions/
    batch.save()
