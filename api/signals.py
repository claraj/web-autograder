from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ProgrammingClass, Grade
import logging

log = logging.getLogger(__name__)

@receiver(pre_save, sender=Grade)
def generate_github_url(sender, **kwargs):
    grade_instance = kwargs['instance']

    # github URL is
    # https://github.com/ORG/ASSIGNMENTNAME-STUDENTGITHUBID

    if not grade_instance.assignment or not grade_instance.student:
        return

    grade_instance.github_url = 'https://github.com/%s/%s-%s' % ( grade_instance.assignment.github_org , grade_instance.assignment.github_base , grade_instance.student.github_id)
    print('generated student github url = ', grade_instance.github_url, grade_instance)



@receiver(pre_save, sender=ProgrammingClass)
def create_human_readable_semester_code(sender, **kwargs):
    print('SIGNAL REC HELLO', kwargs)
    class_instance = kwargs['instance']
    class_instance.semester_human_string = humanCode(class_instance.semester_code)

# this duplicates the receiver decorator on the function (?)
pre_save.connect(create_human_readable_semester_code, sender=ProgrammingClass)


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
