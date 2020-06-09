from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import *

from example.models import *


def _tupleslist_get(tl, key):
    for t in tl:
        if t[0] == key:
            return t[1]
    return None


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


class Card(Model):
    def __str__(self):
        return "{} {}".format(_tupleslist_get(self.GENDERS, self.gender), self.word)

    GENDERS = [
        ('M', 'Der'),
        ('F', 'Die'),
        ('N', 'Das')
    ]

    lesson = ForeignKey(
        Lesson, related_name="cards", on_delete=CASCADE)
    word = CharField(max_length=64)
    gender = CharField(max_length=1, choices=GENDERS)


class Meaning(Model):
    def __str__(self):
        return "{}[{}]: {}".format(str(self.card), self.language_code, self.meaning[:16])

    card = ForeignKey(Card, related_name="meanings", on_delete=CASCADE)
    # language codes can be: en, en-us, ru-ru, etc
    language_code = CharField(max_length=5)
    # Put this meaning in any order, lowest shown first
    order = SmallIntegerField(default=0)
    # Term that is added to the meaning in italic
    term = CharField(max_length=32, blank=True)
    meaning = CharField(max_length=192)
