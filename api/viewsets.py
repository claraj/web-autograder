from rest_framework import viewsets
from .models import Assignment, Student, GraderModule, Grade, Attributes, ProgrammingClass
from .serializers import AssignmentSerializer, StudentSerializer, ProgrammingClassSerializer, GraderModuleSerializer, GradeSerializer, AttributesSerializer
from django_filters.rest_framework import DjangoFilterBackend

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by('week').order_by('-programming_class__semester_code')
    serializer_class = AssignmentSerializer
    filter_fields = ('week', 'programming_class')

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('name').order_by('-programming_class__semester_code')
    serializer_class = StudentSerializer
    filter_fields = ('name', 'programming_class')

class ProgrammingClassViewSet(viewsets.ModelViewSet):
    queryset = ProgrammingClass.objects.all().order_by('-semester_code')
    serializer_class = ProgrammingClassSerializer

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all().order_by('student').order_by('assignment.week')
    serializer_class = GradeSerializer
    filter_fields = ('student', 'assignment')

class GraderModuleViewSet(viewsets.ModelViewSet):
    queryset = GraderModule.objects.all().order_by('name')
    serializer_class = GraderModuleSerializer

class AttributesViewSet(viewsets.ModelViewSet):
    queryset = Attributes.objects.all()
    serializer_class = AttributesSerializer
