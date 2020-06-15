from django.contrib.auth.models import User, Group
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from userprofile.utils import get_language_code


class UserSerializer(ModelSerializer):
    language_code = SerializerMethodField("get_language_code")
    is_editor = SerializerMethodField("get_is_editor")

    def get_language_code(self, user):
        return get_language_code(user)

    def get_is_editor(self, user):
        try:
            editors = Group.objects.get(name="Editors")
        except Group.DoesNotExist:
            # If editors group does not exist
            # we only enable staff (incl. superusers)
            return user.is_staff

        needed_perms = [perm.content_type.app_label + '.' + perm.codename
                        for perm in editors.permissions.all()]

        return user.has_perms(needed_perms)

    class Meta:
        model = User
        fields = ['id', 'username', 'language_code', 'is_editor']
