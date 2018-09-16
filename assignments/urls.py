from django.urls import path
from . import views
from django.views.generic import TemplateView

#TemplateView.as_view(template_name='student.html')),

urlpatterns = [
    path('', TemplateView.as_view(template_name='assignments/index.html') ),
]
