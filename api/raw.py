from .models import Assignment
from .serializers import AssignmentSerializer
from rest_framework import generics

from .serializers import StudentSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework.parsers import BaseParser
from rest_framework.exceptions import MethodNotAllowed

from django.views import View

from .models import Student
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .parsers import PlainTextParser

import csv

def process_raw(data):
    return 'hello!'


from django.views.decorators.http import require_http_methods

@csrf_exempt  # TODO remove
@require_http_methods(['POST'])
def upload_raw(request):
    data = request.body.decode('utf-8')

    print('body', type(request.body))
    print('data', type(data), data)

    errors = []
    students_created = 0

    if not request.body:
        errors += ['No raw data provided']

    else:

        # deal with this as string, process, save .
        lines = data.split('\n')
        reader = csv.reader(lines)
        for (index, row) in enumerate(reader):
            try:
                student = makeStudent(row, index)
                student.save()
                students_created += 1
                print('student saved', student)
            except Exception as e:
                print(e)
                errors += [ 'line %d: %s' % (index, e) ]

    response = { 'created': students_created, 'errors': errors}
    return JsonResponse(response)


class RawStudentDataException(Exception):
    pass


def makeStudent(row, id):
    if not row:
        raise RawStudentDataException('No data in line')
    # if not row[0:1]:
    #     raise RawStudentDataException('Name is required')

    keys = ['name', 'github_id', 'org_id', 'star_id' ]
    vals = row
    args = dict(zip(keys, vals))
    student = Student(**args)
    student.full_clean()  # raises exception if validation problem
    return student
