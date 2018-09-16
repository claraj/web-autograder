from rest_framework import routers
from students.viewsets import StudentViewSet
from assignments.viewsets import AssignmentViewSet

router = routers.DefaultRouter()
router.register(r'student', StudentViewSet)
router.register(r'assignment', AssignmentViewSet)


urlpatterns = router.urls
