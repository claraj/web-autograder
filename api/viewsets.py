from rest_framework import viewsets
from .models import Assignment, Student, GradingBatch, Grade, Attributes, ProgrammingClass
from .serializers import AssignmentSerializer, StudentSerializer, ProgrammingClassSerializer, GradingBatchSerializer, GradeSerializer, AttributesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.db.models.functions import Lower


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by('-programming_class__semester_code', Lower('week'))
    serializer_class = AssignmentSerializer
    filter_fields = ('week', 'programming_class')


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-programming_class__semester_code', Lower('name'))
    serializer_class = StudentSerializer
    filter_fields = ('name', 'programming_class', 'active')


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

    @action(methods=['delete'], detail=False, url_path='deleteMany')
    def deleteMany(self, request):
        print(request)
        for id in request.data:
            GradingBatch.objects.get(id=id).delete()



class AttributesViewSet(viewsets.ModelViewSet):
    queryset = Attributes.objects.all()
    serializer_class = AttributesSerializer
