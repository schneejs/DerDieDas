from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from battery.serializers import BatterySerializer
from card.models import *
from example.serializers import ExamplesSerializer


class MeaningSerializer(ModelSerializer):
    class Meta:
        model = Meaning
        fields = ['id', 'term', 'meaning', 'order', 'language_code']


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'gender', 'second_gender', 'word']
