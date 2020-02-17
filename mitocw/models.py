# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Courses(models.Model):
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    course_number = models.CharField(primary_key=True, max_length=15)
    semester = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=400)
    level = models.CharField(max_length=25)
    features = models.CharField(max_length=300, blank=True, null=True)
    complete_video = models.BooleanField(blank=True, null=True)
    complete_audio = models.BooleanField(blank=True, null=True)
    other_video = models.BooleanField(blank=True, null=True)
    other_audio = models.BooleanField(blank=True, null=True)
    online_textbooks = models.BooleanField(blank=True, null=True)
    complete_lectures = models.BooleanField(blank=True, null=True)
    assesments_with_solution = models.BooleanField(blank=True, null=True)
    student_projects = models.BooleanField(blank=True, null=True)
    instructor_insights = models.BooleanField(blank=True, null=True)
    instructors = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courses'
        unique_together = (('course_number', 'semester'),)
