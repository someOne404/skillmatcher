# Generated by Django 2.1.7 on 2019-04-03 00:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_match', '0002_auto_20190402_2042'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]