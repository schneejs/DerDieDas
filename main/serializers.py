from rest_framework.serializers import ModelSerializer
from main.models import Card, Lesson
from battery.serializers import BatterySerializer
from example.serializers import ExamplesSerializer


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


class LessonFullSerializer(ModelSerializer):
    """
    Full serializer that includes cards
    """
    cards = CardSerializer(many=True)
    

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'difficulty', 'cards']
