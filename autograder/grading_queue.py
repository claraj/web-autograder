from api.models import Student, Assignment, Grade, GradingBatch, ProgrammingClass
from grading_module import ag
from django.db.models import F
import json
from datetime import datetime
import re

from django_q.tasks import async_task, result


def queue_grading_task(batch, assignment_id, student_id, class_id):
    print(f'hello from queue launcher! batch {batch}')
    task_id = async_task(start_grader, batch, assignment_id, student_id, class_id, hook=save_result)


def start_grader(batch, assignment_id, student_id, class_id):

    print('INVOKE GRADER GO hello this is real grader')

    student = Student.objects.get(pk=student_id)
    assignment = Assignment.objects.get(pk=assignment_id)

    print('class', class_id)
    programming_class = ProgrammingClass.objects.get(pk=class_id)
    result = ag.grade(assignment, student)

    print('grader results are', result)

    if not result['success']:
        # These are programatic errors - like the docker config is wrong or some other coding error
        # Probably my problem
        print('ERROR grading:', result['error'] )
        err = result['error']
        return {
            'error': result['error'],
            'batch': batch,
            'assignment_id': assignment_id,
            'student_id': student_id,
            'programming_class_id': class_id,
            'score': 0,
            'generated_report': json.dumps({ 'error': f'Error running grader because {err}' }), # TODO format?
            'github_commit_hash': None
        }

    # Errors like - code doesn't compile, repo not found... save in the Grade object anyway so client can display

    report_result = result['report']
    score = result['score']
    github_commit_hash = result['sha']


    return {
        'error': None,
        'batch': batch,
        'assignment_id': assignment_id,
        'student_id': student_id,
        'programming_class_id': class_id,
        'score': score,
        'generated_report': report_result, # Formatted as JSON string, although this module doesn't need to care.
        'github_commit_hash': github_commit_hash
    }



def save_result(task):

    if task.success:

        result = task.result

        if result:

            print(f'HELLO FROM HOOK this task result is {result}')
            save_grade(result)

        else:
            # get error message and report in some way.
            print('THIS IS HOOK there was error, ', result['error'])

    else:
        print('THIS IS HOOK task was not succesful, nothing saved')


    # And increment number of things processed in this batch
    batch = GradingBatch.objects.get(id=result['batch'])
    batch.processed = F('processed') + 1  #https://docs.djangoproject.com/en/2.1/ref/models/expressions/
    batch.save()


def save_grade(result):

    # Is there another older result for this student and assignment?
    # If so, copy any comments and adjusted grades ( for Q and for overall) to this new Grade.generated_report
    # Include timestamps e.g. 11/04/2019-08:40 This code was ok.

    print('saving grade with result', result)

    # most_recent_previous_grade_qs = Grade.objects   \
    # .filter(student_id=result['student_id'], assignment_id=result['assignment_id'])  \
    # .order_by('-date').all()[:1]  \
    #
    # print('grade before this one? ', most_recent_previous_grade_qs)
    #
    # if most_recent_previous_grade_qs:
    #     latest_report = result['generated_report']
    #     previous_report = most_recent_previous_grade_qs.get().generated_report
    #     updated_report = forward_comments(previous_report, latest_report)
    #     result['generated_report'] = updated_report

    grade = Grade(**result)
    grade.save()


# def forward_comments(prev, new):
#
#     now = datetime.now()
#     timestamp = now.strftime('%m/%d/%y %I:%M%p ')   # 12/31/18 4.30pm
#
#     print(prev, '\n\n')
#     print(next, '\n\n')
#
#     prev_rep = json.loads(prev)
#     new_rep = json.loads(new)
#
#     print(prev_rep, '\n\n')
#     print(new_rep, '\n\n')
#
#     prev_questions = prev_rep['question_reports']
#     new_questions = new_rep['question_reports']
#
#     for (pq, nq) in zip(prev_questions, new_questions):
#         if 'adjusted_points' in pq:
#             nq['adjusted_points'] = pq['adjusted_points']
#         if 'instructor_comments' in pq:
#             comments = pq['instructor_comments']
#             print(comments)
#             already_date = re.match(r'^\d\d/\d\d/\d\d', comments)
#             if already_date:
#                 print('already date in comment')
#                 nq['instructor_comments'] = pq['instructor_comments']
#             else:
#                 nq['instructor_comments'] = timestamp + pq['instructor_comments']
#
#     if 'overall_instructor_comments' in prev_rep:
#
#         comments = prev_rep['overall_instructor_comments']
#         # does this start with a date?
#         already_date = re.match(r'^\d\d/\d\d/\d\d', comments)
#         if already_date:
#             new_rep['overall_instructor_comments'] = prev_rep['overall_instructor_comments']
#         else:
#             new_rep['overall_instructor_comments'] = timestamp + prev_rep['overall_instructor_comments']
#
#     print('new rep:', new_rep)
#     return json.dumps(new_rep)
