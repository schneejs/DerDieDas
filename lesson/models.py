from django.db.models import *


class Lesson(Model):
    def __str__(self):
        return self.name

    DIFFICULTIES = [
        ('J', 'Easy'),
        ('M', 'Middle'),
        ('S', 'Hard')
    ]
    name = CharField(max_length=64)
    difficulty = CharField(max_length=1, choices=DIFFICULTIES)