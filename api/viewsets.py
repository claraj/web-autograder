from rest_framework import viewsets
from .models import Assignment, Student, GradingBatch, Grade, ProgrammingClass
from .serializers import AssignmentSerializer, StudentSerializer, ProgrammingClassSerializer, GradingBatchSerializer, GradeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.functions import Lower
from django.db.models import Max
from .raw import process_raw


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by(Lower('week'))
    serializer_class = AssignmentSerializer
    filter_fields = ('week',)



class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by(Lower('name'))
    serializer_class = StudentSerializer
    filter_fields = ('name', 'active')

    @action(methods=['post'], detail=False, url_path='raw')
    def raw_upload(request):
        try:
            process_raw(request.data)
        except Exception as e:
            return HttpResponseBadRequest('Error processing raw data ' + e.message)


class ProgrammingClassViewSet(viewsets.ModelViewSet):
    queryset = ProgrammingClass.objects.all().order_by('-semester_code')
    serializer_class = ProgrammingClassSerializer

    @action(methods=['get'], detail=True, url_path='students')
    def students_for_class(self, request, pk=None):
        students = Student.objects.filter(programming_classes__id=pk).order_by('name')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


    @action(methods=['get'], detail=True, url_path='assignments')
    def assignments_for_class(self, request, pk=None):
        assignments = Assignment.objects.filter(programming_classes__id=pk).order_by('week')
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)



class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all().order_by('student.name').order_by('assignment')
    serializer_class = GradeSerializer
    filter_fields = ('student', 'assignment', 'batch', 'id')

    @action(methods=['get'], detail=False, url_path='latestGrades')
    def latestGradesForStudent(self, request):
        """ Get latest grade objects for a student, for each individual assignment on record.
        http://127.0.0.1:8000/api/grade/latestGrades/?student=10&programming_class=3
         """
        student = request.query_params['student']
        programmingClass = request.query_params['programming_class']

        latest_by_assignment = Grade.objects.raw("""select *
        from api_grade g1
        where date = (
            select max(g2.date)
            from api_grade g2
            where student_id = %s
            and programming_class_id = %s
            and g1.assignment_id = g2.assignment_id
            )""", [student, programmingClass])

        serializer = GradeSerializer(latest_by_assignment, many=True)
        return Response(serializer.data)



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
