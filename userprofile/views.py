from django.http import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from userprofile.serializers import *
from django.contrib.auth.models import User


class ProfileByUsername(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "User {} not found".format(username)},
                status=404
            )
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "User {} not found".format(username)},
                status=404
            )
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)