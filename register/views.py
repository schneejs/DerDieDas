from re import compile

from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lesson.utils import settings

EMAIL_REGEX = compile(r'^[^@]+@[^@]+\.[^@]+$')


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
            first_name, last_name = None, None
        # Check that input is correct
        if type(username) is str and len(username) >= 5 and username.isascii() and username.isalnum() \
                and (email is None or EMAIL_REGEX.fullmatch(email) is not None):  # email is correct or NULL
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return Response(status=201)
        else:
            # Frontend should handle checking input
            return Response(status=400)
