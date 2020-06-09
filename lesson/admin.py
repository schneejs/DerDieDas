from django.contrib import admin
from lesson.models import *


[admin.site.register(model) for model in [Lesson, Card, Meaning]]