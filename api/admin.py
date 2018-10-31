from django.contrib import admin
from .models import Student, Assignment, ProgrammingClass, GradingBatch, Grade

admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(ProgrammingClass)
admin.site.register(GradingBatch)
admin.site.register(Grade)
