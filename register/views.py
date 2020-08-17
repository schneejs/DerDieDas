from re import compile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lesson.utils import settings
from userprofile.serializers import UserSerializer


class Languages(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        languages = settings()["LANGUAGES"]
        return Response(languages)


class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data["username"]
        try:
            email = request.data["email"]
        except KeyError:
            email = None
        password = request.data["password"]
        if ("first_name" in request.data):
            first_name = request.data["first_name"]
            try:
                last_name = request.data["last_name"]
            except KeyError:
                last_name = ""
        else:
            first_name, last_name = '', ''
        # Check that input is correct
        user = User()
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        try:
            user.full_clean()
            user.save()
        except ValidationError as e:
            return Response({"detail": e.message_dict}, status=400)
        return Response(UserSerializer(user).data, status=201)
