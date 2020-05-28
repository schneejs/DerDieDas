from rest_framework.serializers import ModelSerializer
from example.models import *


class ExamplesSerializer(ModelSerializer):
    class Meta:
        model = Example
        fields = ['string']