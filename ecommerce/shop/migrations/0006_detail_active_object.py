# Generated by Django 3.0.8 on 2020-09-14 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200907_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='active_object',
            field=models.BooleanField(default=True),
        ),
    ]
