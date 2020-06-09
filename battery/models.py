from django.contrib.auth.models import User
from django.db import models

from lesson.models import *
from lesson.utils import settings


class Battery(models.Model):
    def __str__(self):
        return "{}[{}]: {}".format(
            self.user.username,
            str(self.card),
            self.level
        )

    user = models.ForeignKey(
        User, related_name="batteries", on_delete=models.CASCADE)
    card = models.ForeignKey(
        Card, related_name="batteries", on_delete=models.CASCADE)
    level = models.SmallIntegerField(validators=[
        # value -1 is needed for buried cards that user doesn't want to study
        MinValueValidator(settings()["MIN_BATTERY_LEVEL"] - 1),
        MaxValueValidator(settings()["MAX_BATTERY_LEVEL"])
    ])
    last_modified = models.DateTimeField(auto_now=True)
