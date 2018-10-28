from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import ProgrammingClass, Grade
import logging
from datetime import datetime
import json
import re

log = logging.getLogger(__name__)


@receiver(post_save, sender=Grade)
def copy_previous_comments(sender, **kwargs):

    if not kwargs['created']:
        print('this is an update.')
        return

    grade = kwargs['instance']

    most_recent_previous_grade = Grade.objects.most_recent(grade.student.id, grade.assignment.id)

    print('SIGNAL grade before this one? ', most_recent_previous_grade, most_recent_previous_grade.generated_report) # TODO this is none

    if most_recent_previous_grade:
        new_report = grade.generated_report
        previous_report = most_recent_previous_grade.generated_report
        updated_report = forward_comments(previous_report, new_report)
        grade.generated_report = updated_report
        print(grade.generated_report)
        grade.save()

    print('have (perhaps?) copied prev comments forwards')


@receiver(pre_save, sender=Grade)
def generate_github_url(sender, **kwargs):
    grade = kwargs['instance']

    # github URL is  https://github.com/ORG/ASSIGNMENTNAME-STUDENTGITHUBID

    if not grade.assignment or not grade.student:
        return

    grade.student_github_url = 'https://github.com/%s/%s-%s' % ( grade.assignment.github_org , grade.assignment.github_base , grade.student.github_id)
    print('generated student github url = ', grade.student_github_url, grade)


@receiver(pre_save, sender=ProgrammingClass)
def create_human_readable_semester_code(sender, **kwargs):
    print('SIGNAL REC HELLO', kwargs)
    class_instance = kwargs['instance']
    class_instance.semester_human_string = humanCode(class_instance.semester_code)


def forward_comments(prev, new):

    now = datetime.now()
    timestamp = now.strftime('%m/%d/%y %I:%M%p ')   # 12/31/18 4.30pm

    print(prev, '\n\n')
    print(next, '\n\n')

    prev_rep = json.loads(prev)
    new_rep = json.loads(new)

    print(prev_rep, '\n\n')
    print(new_rep, '\n\n')

    prev_questions = prev_rep['question_reports']
    new_questions = new_rep['question_reports']

    for (pq, nq) in zip(prev_questions, new_questions):
        if 'adjusted_points' in pq:
            nq['adjusted_points'] = pq['adjusted_points']
        if 'instructor_comments' in pq:
            comments = pq['instructor_comments']
            print(comments)
            already_date = re.match(r'^\d\d/\d\d/\d\d', comments)
            if already_date:
                print('already date in comment')
                nq['instructor_comments'] = pq['instructor_comments']
            else:
                nq['instructor_comments'] = timestamp + pq['instructor_comments']

    if 'overall_instructor_comments' in prev_rep:

        comments = prev_rep['overall_instructor_comments']
        # does this start with a date?
        already_date = re.match(r'^\d\d/\d\d/\d\d', comments)
        if already_date:
            new_rep['overall_instructor_comments'] = prev_rep['overall_instructor_comments']
        else:
            new_rep['overall_instructor_comments'] = timestamp + prev_rep['overall_instructor_comments']

    print('new rep after updates:', new_rep)
    return json.dumps(new_rep)




def humanCode(numberCode):
    """ convert 201805 to Summer 2019 """

    if not numberCode:
        return

    try :
        sem_codes = { '01': 'Fall', '03': 'Spring', '05': 'Summer' }

        yearStr = numberCode[0:4]
        semester_code = numberCode[4:6]

        numYear = int(yearStr)
        semText = sem_codes[semester_code]
        if semester_code in ['03', '05']:
            numYear += 1
        return '%s %s' % (semText, numYear)
    except Exception as e:
        log.warning('Semester code %s could not be converted to human readable because %s' % (numberCode, e))
