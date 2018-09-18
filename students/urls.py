from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('raw/', views.upload_raw, name="rawData"),
    path('', TemplateView.as_view(template_name='students/index.html') ),
]
