from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from example.models import *


def _tupleslist_get(tl, key):
    for t in tl:
        if t[0] == key:
            return t[1]
    return None


class Lesson(models.Model):
    def __str__(self):
        return self.name

    DIFFICULTIES = [
        ('J', 'Easy'),
        ('M', 'Middle'),
        ('S', 'Hard')
    ]
    name = models.CharField(max_length=64)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)


class Card(models.Model):
    def __str__(self):
        return "{} {}".format(_tupleslist_get(self.GENDERS, self.gender), self.word)

    GENDERS = [
        ('M', 'Der'),
        ('F', 'Die'),
        ('N', 'Das')
    ]

    lesson = models.ForeignKey(
        Lesson, related_name="cards", on_delete=models.CASCADE)
    word = models.CharField(max_length=64)
    gender = models.CharField(max_length=1, choices=GENDERS)
