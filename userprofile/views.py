from django.http import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from userprofile.serializers import *
from django.contrib.auth.models import User


class ProfileByUsername(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                data="User {} not found".format(username),
                status=404, content_type="text/plain"
            )
        user_serializer = UserSerializer(user)
        user_json = JSONRenderer().render(user_serializer.data)
        return Response(data=user_json, status=200, content_type="application/json")
