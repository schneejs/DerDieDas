# Generated by Django 3.0.6 on 2020-05-31 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_meaning'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('battery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battery',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batteries', to='main.Card'),
        ),
        migrations.AlterField(
            model_name='battery',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batteries', to=settings.AUTH_USER_MODEL),
        ),
    ]
