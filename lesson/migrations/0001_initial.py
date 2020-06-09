# Generated by Django 3.0.6 on 2020-06-09 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('difficulty', models.CharField(choices=[('J', 'Easy'), ('M', 'Middle'), ('S', 'Hard')], max_length=1)),
            ],
        ),
    ]
