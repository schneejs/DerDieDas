from enum import IntEnum
from random import choice, random, sample

from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
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
        lesson = get_object_or_404(Lesson, pk=lesson_pk)
        cards = Card.objects.filter(lesson=lesson)
        card_serializer = CardSerializer(cards, many=True)
        return Response(card_serializer.data)


class CreateCardView(APIView):
    permission_classes = [IsEditor]

    def post(self, request):
        try:
            card_raw = {
                "lesson": get_object_or_404(Lesson, pk=int(request.data["lesson"])),
                "word": request.data["word"],
                "gender": request.data["gender"],
                "second_gender": request.data["second_gender"]
            }
            if request.data["word"] == "" \
            or card_raw["gender"] not in 'MFN' \
            or not (card_raw["second_gender"] in 'MFN' \
            or card_raw["second_gender"] == ''):
                raise ValueError
        except (KeyError, ValueError):
            return Response({"detail": "Wrong data"}, status=400)
        card = Card.objects.create(**card_raw)
        return Response(CardSerializer(card).data, status=201)

class CardView(RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsEditor]


# TODO: separate these two methods to make it work in urlpatterns
class MeaningView(APIView):
    permission_classes = [IsEditor]

    def get(self, request, card_pk=None):
        if card_pk:
            meanings = Meaning.objects.filter(card=card_pk)
        else:
            meanings = Meaning.objects.all()
        return Response(MeaningSerializer(meanings, many=True).data)

    def post(self, request):
        if "card_id" not in request.data or not str(request.data["card_id"]).isdigit() \
        or "card_id" in request.data and len(Card.objects.filter(pk=request.data['card_id'])) == 0:
            return Response({"detail": "Card ID is missing or does not exist"}, status=400)
        if "language_code" not in request.data \
        or "language_code" in request.data and request.data["language_code"] not in settings()['LANGUAGES'].keys():
            return Response({"detail": "Wrong language code"}, status=400)
        if "meaning" not in request.data:
            return Response({"detail": "Meaning field is required"}, status=400)
        if type(request.data) is dict:
            meaningArgs = request.data
        # request.data can be QueryDict because
        # the tests send 'application/x-www-form-urlencoded'
        # and browser's axios sends JSON
        elif type(request.data) is QueryDict:
            meaningArgs = request.data.dict()
        meaningArgs["card"] = Card.objects.get(pk=int(meaningArgs["card_id"]))
        del meaningArgs["card_id"]
        meaning = Meaning.objects.create(**meaningArgs)
        return Response(MeaningSerializer(meaning).data, status=201)

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
        card_serializer = BuriedCardSerializer(
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
