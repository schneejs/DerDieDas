from django.contrib.auth.models import User
from django.db.models import *


class LanguageCode(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    language_code = CharField(
        max_length=5,
        default="en"
    )
