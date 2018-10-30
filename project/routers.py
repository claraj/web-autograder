from rest_framework import routers

from api import viewsets

from django.urls import path

router = routers.DefaultRouter()

router.register(r'student', viewsets.StudentViewSet)
router.register(r'assignment', viewsets.AssignmentViewSet)
router.register(r'grade', viewsets.GradeViewSet)
router.register(r'gradingbatch', viewsets.GradingBatchViewSet)
router.register(r'programmingclass', viewsets.ProgrammingClassViewSet)
