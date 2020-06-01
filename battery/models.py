from django.contrib.auth.models import User
from django.db import models

from main.models import *
from main.utils import settings


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
        MinValueValidator(settings()["MIN_BATTERY_LEVEL"]),
        MaxValueValidator(settings()["MAX_BATTERY_LEVEL"])
    ])
    last_modified = models.DateTimeField(auto_now=True)
