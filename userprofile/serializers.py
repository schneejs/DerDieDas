from django.contrib.auth.models import User, Group
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from userprofile.utils import get_language_code
from userprofile.permissions import is_user_editor


class UserSerializer(ModelSerializer):
    language_code = SerializerMethodField("get_language_code")
    is_editor = SerializerMethodField("is_user_editor")

    def get_language_code(self, user):
        return get_language_code(user)

    def is_user_editor(self, user):
        return is_user_editor(user)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'language_code', 'is_editor']
