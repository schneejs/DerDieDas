# Generated by Django 3.0.7 on 2020-06-17 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0002_lesson_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
