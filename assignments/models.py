from django.db import models


from django.apps import apps

# ProgrammingClass = apps.get_model('autograder', 'ProgrammingClass')


# class Assignment(models.Model):
#     # programming_class = models.ForeignKey('autograder.ProgrammingClass', on_delete=models.DO_NOTHING, null=True, blank=True)
#     # programming_class = models.ForeignKey(ProgrammingClass, on_delete=models.DO_NOTHING, null=True, blank=True)
#     week = models.IntegerField()
#     github_base = models.CharField(max_length=200)      # e.g. week-0-variables
#     instructor_repo = models.CharField(max_length=200)  # eg. https://github.com/minneapolis-edu/JAG_0
#     d2l_gradebook_url = models.CharField(max_length=200, blank=True, null=False)
#     grader = models.ForeignKey('autograder.GraderModule', on_delete=models.DO_NOTHING)
