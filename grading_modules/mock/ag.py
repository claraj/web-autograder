import random
import time

def grade(assignment, student):
    print('grader placeholder')
    time.sleep(1)
    return assignment + ' ' + student + ' ' + random.choice([
        'great',
        'super',
        'no code',
        'try harder',
        'pretty good'
    ])
