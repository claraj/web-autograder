# from django.urls import path
from django.conf.urls import url, include
from . import views
from django.views.generic import TemplateView
import django_eventstream

#TemplateView.as_view(template_name='student.html')),

urlpatterns = [
    url('^grader/', views.grader_start),
    # path('students/raw/', views.upload_raw, name="rawData"),
    # url('^testing/(?P<channel>\w+)', views.testing_sse),
    url('^progress/', views.grader_get_progress)
]
