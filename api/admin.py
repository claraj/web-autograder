from django.contrib import admin
from .models import Student, Assignment, ProgrammingClass, GraderModule, Grade, Attributes

admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(ProgrammingClass)
admin.site.register(GraderModule)
admin.site.register(Grade)
admin.site.register(Attributes)
