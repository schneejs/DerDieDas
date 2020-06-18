from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from example.models import *
from example.serializers import *
from userprofile.permissions import IsEditor


class ExampleView(RetrieveUpdateDestroyAPIView):
    queryset = Example.objects.all()
    serializer_class = ExamplesSerializer
    permission_classes = [IsEditor]