from django.contrib.auth.models import Group, User
from rest_framework.permissions import BasePermission


def is_user_editor(user):
    try:
        editors = Group.objects.get(name="Editors")
    except Group.DoesNotExist:
        # If editors group does not exist
        # we only enable staff (incl. superusers)
        return user.is_staff

    needed_perms = [perm.content_type.app_label + '.' + perm.codename
                    for perm in editors.permissions.all()]

    return user.has_perms(needed_perms)


class IsEditor(BasePermission):
    """
    Does user belong to Editors group
    """

    def has_permission(self, request, view):
        return is_user_editor(request.user)
