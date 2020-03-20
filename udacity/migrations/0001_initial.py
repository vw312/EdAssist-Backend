# Generated by Django 3.0.4 on 2020-03-18 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('school', models.CharField(blank=True, max_length=50, null=True)),
                ('paid', models.BooleanField()),
                ('difficulty', models.IntegerField()),
                ('url', models.CharField(max_length=400)),
            ],
            options={
                'db_table': 'courses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'skills',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SkillsCovered',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'skills_covered',
                'managed': False,
            },
        ),
    ]
