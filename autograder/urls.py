# from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('^grader/', views.grader_start),
    url('^progress/', views.grader_get_progress),
    url('^regrade/', views.regrade)
]
