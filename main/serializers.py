from rest_framework import serializers
from main.models import *


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['gender', 'word']


class LessonSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'difficulty', 'cards']