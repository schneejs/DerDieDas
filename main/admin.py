from django.contrib import admin
from main.models import *


[admin.site.register(model) for model in [Lesson, Card, Meaning]]