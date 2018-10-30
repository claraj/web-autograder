from rest_framework import viewsets
from .models import Assignment, Student, GradingBatch, Grade, Attributes, ProgrammingClass
from .serializers import AssignmentSerializer, StudentSerializer, ProgrammingClassSerializer, GradingBatchSerializer, GradeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.functions import Lower


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by(Lower('week'))
    serializer_class = AssignmentSerializer
    filter_fields = ('week',)



class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by(Lower('name'))
    serializer_class = StudentSerializer
    filter_fields = ('name', 'active')



class ProgrammingClassViewSet(viewsets.ModelViewSet):
    queryset = ProgrammingClass.objects.all().order_by('-semester_code')
    serializer_class = ProgrammingClassSerializer

    @action(methods=['get'], detail=True, url_path='students')
    def students_for_class(self, request, pk=None):
        students = Student.objects.filter(programming_classes__id=pk)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


    @action(methods=['get'], detail=True, url_path='assignments')
    def assignments_for_class(self, request, pk=None):
        assignments = Assignment.objects.filter(programming_classes__id=pk)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)



class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all().order_by('student').order_by('assignment.week')
    serializer_class = GradeSerializer
    filter_fields = ('student', 'assignment', 'batch', 'id')



class GradingBatchViewSet(viewsets.ModelViewSet):
    queryset = GradingBatch.objects.all().order_by('-date')
    serializer_class = GradingBatchSerializer

    @action(methods=['patch'], detail=False, url_path='deleteMany')
    def deleteMany(self, request):
        if not 'ids' in request.data:
            return Response('no ids to delete', status=status.HTTP_400_BAD_REQUEST)
        for id in request.data['ids']:
            GradingBatch.objects.get(id=id).delete()
        return Response('ok')  # ok,
