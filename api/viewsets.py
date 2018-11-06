from rest_framework import viewsets
from .models import Assignment, Student, GradingBatch, Grade, ProgrammingClass
from .serializers import AssignmentSerializer, StudentSerializer, ProgrammingClassSerializer, GradingBatchSerializer, GradeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.functions import Lower
from django.db.models import Max
from .raw import process_raw
from django.shortcuts import get_object_or_404


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

    @action(methods=['get', 'post', 'patch'], detail=True, url_path='students')
    def students_for_class(self, request, pk=None):

        if request.method == 'GET':
            students = Student.objects.filter(programming_classes__id=pk).order_by('name')
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)

        # add students to class
        if request.method == 'POST':
            students = request.data.get('studentIds')
            programming_class = get_object_or_404(ProgrammingClass, pk=pk)
            for student in students:
                programming_class.student_set.add(student)
            programming_class.save()
            return Response(ProgrammingClassViewSet.serializer_class(programming_class).data)

        # Remove students from class, modify student_set
        if request.method == 'PATCH':
            students = request.data.get('studentIds')
            programming_class = get_object_or_404(ProgrammingClass, pk=pk)
            for student in students:
                programming_class.student_set.remove(student)
            programming_class.save()
            return Response(ProgrammingClassViewSet.serializer_class(programming_class).data)



    @action(methods=['get', 'post', 'patch'], detail=True, url_path='assignments')
    def assignments_for_class(self, request, pk=None):
        if request.method == 'GET':
            assignments = Assignment.objects.filter(programming_classes__id=pk).order_by('week')
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            assignments = request.data.get('assignmentIds')
            programming_class = get_object_or_404(ProgrammingClass, pk=pk)
            for assignment in assignments:
                programming_class.assignment_set.add(assignment)
            programming_class.save()
            return Response(ProgrammingClassViewSet.serializer_class(programming_class).data)

        # Remove assignments
        if request.method == 'PATCH':
            assignments = request.data.get('assignmentIds')
            programming_class = get_object_or_404(ProgrammingClass, pk=pk)
            for assignment in assignments:
                programming_class.assignment_set.remove(assignment)
            programming_class.save()
            return Response(ProgrammingClassViewSet.serializer_class(programming_class).data)


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


    @action(methods=['GET'], detail=True)
    def students(self, request, pk=None):
        # grades = Grade.objects.filter(batch=batch_pk).distinct('student')  # But not in SQLite!
        grades = Grade.objects.filter(batch=pk)
        all_student_ids = [ grade.student.id for grade in grades ]
        unique_student_ids = set(all_student_ids)
        students = list(Student.objects.filter(id__in=unique_student_ids))
        return Response(StudentSerializer(students, many=True).data)


    @action(methods=['GET'], detail=True)
    def assignments(self, request, pk=None):
        grades = Grade.objects.filter(batch=pk)
        all_assignment_ids = [ grade.assignment.id for grade in grades ]
        unique_assignment_ids = set(all_assignment_ids)
        assignments = list(Assignment.objects.filter(id__in=unique_assignment_ids))
        return Response(AssignmentSerializer(assignments, many=True).data)
