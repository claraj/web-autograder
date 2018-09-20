from rest_framework import routers

from api.viewsets import AssignmentViewSet, StudentViewSet

from django.urls import path

router = routers.DefaultRouter()

router.register(r'student', StudentViewSet)
# router.register(r'upload', post_raw)
router.register(r'assignment', AssignmentViewSet)
