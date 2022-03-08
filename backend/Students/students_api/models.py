from django.db import models


class Students(models.Model):
    name = models.TextField()
    stud_date = models.DateField()
    stud_group = models.TextField()
    cours = models.IntegerField()
    individual = models.BooleanField()
    photography = models.ImageField(upload_to='images/')


class Sections(models.Model):
    section = models.TextField()


class StudentsSections(models.Model):
    section = models.ForeignKey(Sections, on_delete=models.CASCADE)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
