from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ProgrammingClass
import logging

log = logging.getLogger(__name__)

print('SIGNAL HELLO')


@receiver(pre_save, sender=ProgrammingClass)
def create_human_readable_semester_code(sender, **kwargs):
    print('SIGNAL REC HELLO', kwargs)
    instance = kwargs['instance']
    instance.semester_human_string = humanCode(instance.semester_code)

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
