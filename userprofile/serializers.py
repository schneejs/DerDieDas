from django.contrib.auth.models import User
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from userprofile.utils import get_language_code


class UserSerializer(ModelSerializer):
    language_code = SerializerMethodField("get_language_code")

    def get_language_code(self, user):
        return get_language_code(user)

    class Meta:
        model = User
        fields = ['id', 'username', 'language_code']
