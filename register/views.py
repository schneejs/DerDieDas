from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lesson.utils import settings


class Languages(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        languages = settings()["LANGUAGES"]
        return Response(languages)


class SignUp(APIView):
    pass
