from django.db import models


class Example(models.Model):
    """
    Example can be filtered for containing a specific word
    with that one example can be used in many cards
    """
    def __str__(self):
        return self.string[:16]

    string = models.CharField(max_length=256)