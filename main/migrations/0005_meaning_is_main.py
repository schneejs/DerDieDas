# Generated by Django 3.0.6 on 2020-06-02 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_meaning'),
    ]

    operations = [
        migrations.AddField(
            model_name='meaning',
            name='is_main',
            field=models.BooleanField(default=False),
        ),
    ]
