from django.contrib import admin
from .models import ProgrammingClass, GraderModule, Grade
# Register your models here.

admin.site.register(ProgrammingClass)
admin.site.register(GraderModule)
admin.site.register(Grade)
