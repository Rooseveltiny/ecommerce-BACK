# Generated by Django 3.0.8 on 2020-07-21 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20200721_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.UUIDField(blank=True, default=''),
        ),
    ]
