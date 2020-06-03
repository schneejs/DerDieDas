from rest_framework.serializers import ModelSerializer

from battery.serializers import BatterySerializer
from example.serializers import ExamplesSerializer
from main.models import Card, Lesson, Meaning


class MeaningSerializer(ModelSerializer):
    class Meta:
        model = Meaning
        fields = ['term', 'meaning', 'order']


class CardSerializer(ModelSerializer):
    battery = BatterySerializer()
    examples = ExamplesSerializer(many=True)

    class Meta:
        model = Card
        fields = ['gender', 'word', 'battery', 'examples']


class LessonSerializer(ModelSerializer):
    """
    Serializer that should be used for listing lessons
    """
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'difficulty']
