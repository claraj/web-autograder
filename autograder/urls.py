from django.urls import path
from . import views
from django.views.generic import TemplateView

#TemplateView.as_view(template_name='student.html')),

urlpatterns = [
    path('grader', views.grader_placeholder, name="grader_placeholder"),
    # path('students/raw/', views.upload_raw, name="rawData"),
]
