from enum import IntEnum
from random import choice, random, sample

from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from battery.models import Battery
from battery.serializers import BatterySerializer
from card.models import Card, Meaning
from card.serializers import *
from example.models import Example
from example.serializers import ExamplesSerializer
from lesson.models import Lesson
from lesson.serializers import LessonSerializer
from lesson.utils import settings
from userprofile.permissions import IsEditor
from userprofile.utils import get_language_code


class AnswerCard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, card_pk, is_correct):
        min_level = settings()["MIN_BATTERY_LEVEL"]
        max_level = settings()["MAX_BATTERY_LEVEL"]
        card = get_object_or_404(Card, pk=card_pk)
        try:
            battery = Battery.objects.get(card=card, user=request.user)
        except Battery.DoesNotExist:
            # if card exists but there's no corresponding battery
            # then the card was only introduced to the user
            Battery.objects.create(
                user=request.user,
                card=card,
                level=min_level + 1
            )
            return Response()
        if is_correct > 0:
            if battery.level < max_level:
                battery.level += 1
        else:
            if battery.level > min_level:
                battery.level -= 1
        battery.save()
        return Response()


class LessonsCardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lesson_pk):
        cards = Card.objects.filter(lesson=lesson_pk)
        if len(cards) == 0:
            return Response(status=404)
        card_serializer = CardSerializer(cards, many=True)
        return Response(card_serializer.data)


class CardView(RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsEditor]


class MeaningView(RetrieveUpdateDestroyAPIView):
    queryset = Meaning.objects.all()
    serializer_class = MeaningSerializer
    permission_classes = [IsEditor]


class ListBuriedCards(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lesson_pk=None):
        if lesson_pk:
            lesson = get_object_or_404(Lesson, pk=lesson_pk)
            requested_cards = Card.objects.filter(lesson=lesson)
        else:
            requested_cards = Card.objects.all()
        user = request.user
        users_buried_cards_batteries = Battery.objects.filter(
            user=user, level=-1)  # BURIED
        users_buried_cards = [
            battery.card for battery in users_buried_cards_batteries]
        # TODO: optimize this
        requested_users_buried_cards = set(
            requested_cards) & set(users_buried_cards)
        card_serializer = CardSerializer(
            requested_users_buried_cards, many=True)
        return Response(card_serializer.data)


class BuryCard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, card_pk):
        card = get_object_or_404(Card, pk=card_pk)
        try:
            battery = Battery.objects.get(card=card, user=request.user)
        except Battery.DoesNotExist:
            # if card exists but there's no corresponding battery
            # then the card was only introduced to the user
            Battery.objects.create(
                user=request.user,
                card=card,
                level=-1  # BURIED
            )
            return Response()
        battery.level = -1
        battery.save()
        return Response()


class UnburyCard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, card_pk):
        min_level = settings()["MIN_BATTERY_LEVEL"]
        card = get_object_or_404(Card, pk=card_pk)
        try:
            battery = Battery.objects.get(card=card, user=request.user)
        except Battery.DoesNotExist:
            # if card exists but there's no corresponding battery
            # then the card was only introduced to the user
            Battery.objects.create(
                user=request.user,
                card=card,
                level=min_level
            )
            return Response()
        battery.level = min_level
        battery.save()
        return Response()
