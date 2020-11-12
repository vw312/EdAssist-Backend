# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import JSONField


class YoutubeStuff(models.Model):
    youtube_id = models.CharField(max_length=20,primary_key=True)
    caption_name = models.CharField(max_length=100)
    captions = models.TextField()
    important_words = JSONField(blank=True, null=True)

    class Meta:
        # managed = True
        db_table = 'youtube_stuff'
        unique_together = (('youtube_id', 'caption_name'),)


class Courses(models.Model):
    disciplinename = models.CharField(max_length=50)
    subjectid = models.CharField(primary_key=True, max_length=10)
    subjectname = models.CharField(max_length=200)
    institute = models.CharField(max_length=100)
    medium = models.CharField(max_length=20)
    state = models.BooleanField(blank=True, null=True)
    extra_downloads = models.BooleanField(blank=True, null=True)
    coordinators = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courses'


class ExtraDownloads(models.Model):
    subjectid = models.ForeignKey(Courses, models.DO_NOTHING, db_column='subjectid')
    download_link = models.CharField(max_length=400,
                                     primary_key=True)  # not the primary_key.Done so that django doesn't add id in
    # SQL Query
    module_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'extra_downloads'


class Lectures(models.Model):
    subjectid = models.ForeignKey(Courses, models.DO_NOTHING, db_column='subjectid', primary_key=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    youtube_id = models.CharField(max_length=20, blank=True, null=True)
    lecture_number = models.SmallIntegerField()
    video_download = models.CharField(max_length=400, blank=True, null=True)
    pdf_download = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lectures'
        unique_together = (('subjectid', 'lecture_number'),)
