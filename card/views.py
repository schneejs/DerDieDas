from enum import IntEnum
from random import choice, random, sample

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
from userprofile.utils import get_language_code


class AnswerCard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, card_pk, is_correct):
        min_level = settings()["MIN_BATTERY_LEVEL"]
        max_level = settings()["MAX_BATTERY_LEVEL"]
        try:
            card = Card.objects.get(pk=card_pk)
        except Card.DoesNotExist:
            return Response({"detail": "Card not found"}, status=404)
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
        if is_correct > 0:
            if battery.level < max_level:
                battery.level += 1
        else:
            if battery.level > min_level:
                battery.level -= 1
        battery.save()
        return Response()


class BuryCard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, card_pk):
        try:
            card = Card.objects.get(pk=card_pk)
        except Card.DoesNotExist:
            return Response({"detail": "Card not found"}, status=404)
        try:
            battery = Battery.objects.get(card=card, user=request.user)
        except Battery.DoesNotExist:
            # if card exists but there's no corresponding battery
            # then the card was only introduced to the user
            Battery.objects.create(
                user=request.user,
                card=card,
                level=-1 # BURIED
            )
            return Response()
        battery.level = -1
        battery.save()
        return Response()


class UnburyCard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, card_pk):
        min_level = settings()["MIN_BATTERY_LEVEL"]
        try:
            card = Card.objects.get(pk=card_pk)
        except Card.DoesNotExist:
            return Response({"detail": "Card not found"}, status=404)
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
