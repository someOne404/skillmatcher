# Generated by Django 2.1.7 on 2019-02-24 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_match', '0004_auto_20190222_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status_active',
            field=models.BooleanField(default=True),
        ),
    ]
