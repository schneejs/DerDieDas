from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import *

from example.models import *
from lesson.models import Lesson


def _tupleslist_get(tl, key):
    for t in tl:
        if t[0] == key:
            return t[1]
    return None


class Card(Model):
    """
    Model for cards - words with corresponding lesson and gender (up to 2)
    German has a small set of words that have 3 genders which aren't supported:
    https://en.wiktionary.org/wiki/Appendix:German_nouns_which_have_all_three_genders
    """

    def __str__(self):
        first_gender = _tupleslist_get(self.GENDERS, self.gender)
        if self.second_gender is not None:
            return "{}/{} {}".format(
                first_gender,
                _tupleslist_get(self.GENDERS, self.second_gender),
                self.word
            )
        else:
            return "{} {}".format(first_gender, self.word)

    GENDERS = [
        ('M', 'Der'),
        ('F', 'Die'),
        ('N', 'Das')
    ]

    lesson = ForeignKey(
        Lesson, related_name="cards", on_delete=CASCADE)
    word = CharField(max_length=64)
    gender = CharField(max_length=1, choices=GENDERS)
    second_gender = CharField(
        max_length=1, choices=GENDERS, blank=True, default='')


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
