from django.contrib.auth.models import User
from django.http import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
            try:
                language_code = LanguageCode.objects.get(user=user)
                language_code.language_code = request.data["language_code"]
                language_code.save()
            except LanguageCode.DoesNotExist:
                language_code = LanguageCode.objects.create(
                    user=user, language_code=request.data["language_code"])

        return Response()
