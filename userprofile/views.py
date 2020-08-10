from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lesson.utils import settings
from userprofile.models import LanguageCode
from userprofile.serializers import *


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _detect_user(request, username):
        if username == "":
            return request.user
        else:
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                raise Http404

    def get(self, request, username):
        user = self._detect_user(request, username)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    def patch(self, request, username):
        if username is not None and request.user.username != username:
            return Response({"detail": "You're attempting to change another user's data"}, status=403)
        user = self._detect_user(request, username)

        if "language_code" in request.data:
            languages = settings()['LANGUAGES']
            if request.data["language_code"] not in languages:
                return Response({"detail": "This language code is not supported"}, status=400)
            try:
                language_code = LanguageCode.objects.get(user=user)
                language_code.language_code = request.data["language_code"]
                language_code.save()
            except LanguageCode.DoesNotExist:
                language_code = LanguageCode.objects.create(
                    user=user, language_code=request.data["language_code"])
        if "first_name" in request.data:
            user.first_name = request.data["first_name"]
        if "last_name" in request.data:
            user.last_name = request.data["last_name"]
        if "username" in request.data:
            user.username = request.data["username"]
        if "email" in request.data:
            user.email = request.data["email"]

        try:
            user.full_clean()
            user.save()
        except ValidationError as e:
            return Response({"detail": e.message_dict}, status=400)

        return Response(UserSerializer(user).data)
