from rest_framework import viewsets
from .models import Assignment, Student, GradingBatch, Grade, Attributes, ProgrammingClass
from .serializers import AssignmentSerializer, StudentSerializer, ProgrammingClassSerializer, GradingBatchSerializer, GradeSerializer, AttributesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.functions import Lower


class AssignmentViewSet(viewsets.ModelViewSet):
    # queryset = Assignment.objects.all().order_by('-programming_class__semester_code', Lower('week'))
    # serializer_class = AssignmentSerializer
    # filter_fields = ('week', 'programming_class')

    queryset = Assignment.objects.all().order_by(Lower('week'))
    serializer_class = AssignmentSerializer
    filter_fields = ('week',)


class StudentViewSet(viewsets.ModelViewSet):
    # queryset = Student.objects.all().order_by('-programming_class__semester_code', Lower('name'))
    # serializer_class = StudentSerializer
    # filter_fields = ('name', 'programming_class', 'active')

    queryset = Student.objects.all().order_by(Lower('name'))
    serializer_class = StudentSerializer
    filter_fields = ('name', 'active')



class ProgrammingClassViewSet(viewsets.ModelViewSet):
    queryset = ProgrammingClass.objects.all().order_by('-semester_code')
    serializer_class = ProgrammingClassSerializer


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all().order_by('student').order_by('assignment.week')
    serializer_class = GradeSerializer
    filter_fields = ('student', 'assignment', 'batch', 'id')


class GradingBatchViewSet(viewsets.ModelViewSet):
    queryset = GradingBatch.objects.all().order_by('-date')
    serializer_class = GradingBatchSerializer

    @action(methods=['patch'], detail=False, url_path='deleteMany')
    def deleteMany(self, request):
        # print('delete many req', request.data, request.stream)
        if not 'ids' in request.data:
            return Response('no ids to delete', status=status.HTTP_400_BAD_REQUEST)
        for id in request.data['ids']:
            GradingBatch.objects.get(id=id).delete()
        return Response('ok')  # ok,



class AttributesViewSet(viewsets.ModelViewSet):
    queryset = Attributes.objects.all()
    serializer_class = AttributesSerializer
