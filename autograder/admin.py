from django.contrib import admin
from .models import Student, Assignment, Grade
# Register your models here.

admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(Grade)
