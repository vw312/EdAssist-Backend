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
    school = models.CharField(max_length=50, blank=True, null=True)
    paid = models.BooleanField()
    difficulty = models.IntegerField()
    url = models.CharField(max_length=400)

    class Meta:
        managed = False
        db_table = 'courses'
        app_label='udacity'


class Skills(models.Model):
    skill = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'skills'
        app_label='udacity'


class SkillsCovered(models.Model):
    course = models.ForeignKey(Courses, models.DO_NOTHING)
    skill = models.ForeignKey(Skills, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'skills_covered'
        app_label='udacity'
