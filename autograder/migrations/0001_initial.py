# Generated by Django 2.1.1 on 2018-09-18 19:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('github_base', models.CharField(max_length=200)),
                ('instructor_repo', models.CharField(max_length=200)),
                ('d2l_gradebook_url', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_report', models.TextField()),
                ('instructor_comments', models.TextField()),
                ('score', models.DecimalField(decimal_places=3, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='GraderModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=100)),
                ('module', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammingClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='spork appreciation 101', max_length=100)),
                ('semester_code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_id', models.CharField(blank=True, max_length=8, validators=[django.core.validators.RegexValidator('^\\d{8}$', message='MCTC Student ID must be 8 numbers')])),
                ('name', models.CharField(max_length=200)),
                ('github_id', models.CharField(blank=True, max_length=200, validators=[django.core.validators.RegexValidator('^[\\S_-]+$', message='Only letters, numbers, underscores and hyphens.')])),
                ('star_id', models.CharField(blank=True, max_length=8, validators=[django.core.validators.RegexValidator('^[a-z]{2}\\d{4}[a-z]{2}$', message='Star ID must be in the pattern ab1234cd')])),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='grader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autograder.GraderModule'),
        ),
    ]
