from rest_framework import viewsets
from autograder.models import Assignment
from .serializers import AssignmentSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
