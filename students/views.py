from students.models import Student
from students.serializers import StudentSerializer
from rest_framework import viewsets

class StudentListCreate(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('name')
    serializer_class = StudentSerializer
