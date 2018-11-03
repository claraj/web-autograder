# from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('grader/', views.grader_start),
    path('progress/', views.grader_get_progress),
    path('regrade/', views.regrade),
    path('text/<pk>/', views.textReport)
]
