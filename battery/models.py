from django.db import models
from django.contrib.auth.models import User
from main.models import *


class Battery(models.Model):
    def __str__(self):
        return "{}[{}]: {}".format(
            self.user.username,
            str(self.card),
            self.level
        )

    user = models.ForeignKey(User, related_name="batteries", on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name="batteries", on_delete=models.CASCADE)
    level = models.SmallIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(4)
    ])
    last_modified = models.DateTimeField(auto_now=True)