# Generated by Django 3.0.8 on 2020-09-07 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20200903_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('feed_back_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, verbose_name='Ваше имя')),
                ('company', models.CharField(blank=True, max_length=100, verbose_name='Компания')),
                ('email', models.EmailField(max_length=100, verbose_name='Электронная почта')),
                ('phone_number', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('car_type', models.IntegerField(choices=[(1, 'Физическое лицо'), (2, 'Юридическое лицо')], verbose_name='Лицо')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, default='Описания нет', max_length=1000),
        ),
    ]
