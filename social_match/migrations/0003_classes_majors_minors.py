# Generated by Django 2.1.7 on 2019-03-05 05:13

from django.db import migrations
from django.core.management import call_command
import os

def load_classes_fixture(apps, schema_editor):
    fixture = 'class_data'
    call_command('loaddata', fixture, app_label='social_match')


def unload_classes_fixture(apps, schema_editor):
    Course = apps.get_model("social_match", "Course")
    Course.objects.all().delete()


def load_majors_fixture(apps, schema_editor):
    fixture = 'major_data'
    call_command('loaddata', fixture, app_label='social_match')


def unload_majors_fixture(apps, schema_editor):
    Major = apps.get_model("social_match", "Major")
    Major.objects.all().delete()


def load_minors_fixture(apps, schema_editor):
    fixture = 'minor_data'
    call_command('loaddata', fixture, app_label='social_match')


def unload_minors_fixture(apps, schema_editor):
    Minor = apps.get_model("social_match", "Minor")
    Minor.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('social_match', '0007_auto_20190312_1425'),
    ]
    operations = [
        migrations.RunPython(load_classes_fixture, reverse_code=unload_classes_fixture),
        migrations.RunPython(load_majors_fixture, reverse_code=unload_majors_fixture),
        migrations.RunPython(load_minors_fixture, reverse_code=unload_minors_fixture),
    ]
