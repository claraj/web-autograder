from autograder.models import Assignment
from assignments.serializers import AssignmentSerializer
from rest_framework import generics


class AssignmentListCreate(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
