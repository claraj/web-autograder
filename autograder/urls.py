from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home),
    path('spa', TemplateView.as_view(template_name='grader/spa.html'), name='spahome'),
    # path('manage_assignments', views.manage_assignments, name='manage_assignments'),
    # path('manage_students', views.manage_students, name='manage_students'),
    path('grade', views.grade, name="grade"),   # runs the grader.
    path('results/<asgt_id>', views.results, name="results_overview"),
    path('result/<asgt_id>/<student_id>', views.assigment_result, name="assignment_result")

]
