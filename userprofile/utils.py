from django.contrib.auth.models import User


def get_language_code(user):
    try:
        language_code = user.languagecode.language_code
    except:
        language_code = "en"
    return language_code
