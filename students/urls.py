from django.urls import path
from . import views

urlpatterns = [
    path('api/student/', views.StudentListCreate.as_view() ),
]
