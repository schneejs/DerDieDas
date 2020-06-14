from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from battery.serializers import BatterySerializer
from card.models import *
from example.serializers import ExamplesSerializer


class MeaningSerializer(ModelSerializer):
    class Meta:
        model = Meaning
        fields = ['id', 'term', 'meaning', 'order']


class CardSerializer(ModelSerializer):
    gender = SerializerMethodField("get_full_gender")

    def get_full_gender(self, card) -> str:
        return card.gender if card.second_gender is None else card.gender + card.second_gender

    class Meta:
        model = Card
        fields = ['gender', 'word']
