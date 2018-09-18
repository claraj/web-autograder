from rest_framework import routers
from students.viewsets import StudentViewSet

from assignments.viewsets import AssignmentViewSet
from django.urls import path

router = routers.DefaultRouter()
router.register(r'student', StudentViewSet)
# router.register(r'upload', post_raw)
router.register(r'assignment', AssignmentViewSet)
