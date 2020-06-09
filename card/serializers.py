from rest_framework.serializers import ModelSerializer

from battery.serializers import BatterySerializer
from card.models import *
from example.serializers import ExamplesSerializer


class MeaningSerializer(ModelSerializer):
    class Meta:
        model = Meaning
        fields = ['id', 'term', 'meaning', 'order']


class CardSerializer(ModelSerializer):
    battery = BatterySerializer()
    examples = ExamplesSerializer(many=True)

    class Meta:
        model = Card
        fields = ['gender', 'word', 'battery', 'examples']
