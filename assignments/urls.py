from django.urls import path
from . import views

urlpatterns = [
    path('api/assignment/', views.AssignmentListCreate.as_view() ),
]
