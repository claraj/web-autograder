from django.urls import path
from . import views
from django.views.generic import TemplateView

#TemplateView.as_view(template_name='student.html')),

urlpatterns = [
    # path('assignments/raw/', views.upload_raw, name="rawData"),
    # path('students/raw/', views.upload_raw, name="rawData"),

    # todo is this being used here? cos it shouldn't be
    path('spa/', TemplateView.as_view(template_name='grader/spa.html'), name='spahome'),


]
