from rest_framework import routers

from . import viewsets

from django.urls import path

router = routers.DefaultRouter()

router.register(r'student', viewsets.StudentViewSet)
router.register(r'assignment', viewsets.AssignmentViewSet)
router.register(r'attributes', viewsets.AttributesViewSet)
router.register(r'grade', viewsets.GradeViewSet)
router.register(r'gradingbatch', viewsets.GradingBatchViewSet)
router.register(r'programmingclass', viewsets.ProgrammingClassViewSet)
router.register(r'assignment', viewsets.AssignmentViewSet)

# /// TODO register these router from project routers.py
