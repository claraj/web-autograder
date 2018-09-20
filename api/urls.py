from django.urls import path
from . import views
from django.views.generic import TemplateView

#TemplateView.as_view(template_name='student.html')),

urlpatterns = [
    # path('', TemplateView.as_view(template_name='assignments/index.html') ),
    path('raw/', views.upload_raw, name="rawData"),
    # path('students', TemplateView.as_view(template_name='students/index.html') ),
    path('spa/', TemplateView.as_view(template_name='grader/spa.html'), name='spahome'),


]
