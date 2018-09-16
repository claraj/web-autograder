from django.db import models

class Assignment(models.Model):
    # programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.SET_NULL, null=True)
    week = models.IntegerField()
    github_base = models.CharField(max_length=200)      # e.g. week-0-variables
    instructor_repo = models.CharField(max_length=200)  # eg. https://github.com/minneapolis-edu/JAG_0
    d2l_gradebook_url = models.CharField(max_length=200, blank=True, null=True)
