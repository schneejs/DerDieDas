from enum import IntEnum
from random import choice, random, sample

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

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


class ListLessons(ListAPIView):
    """
    View for listing lessons
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class GenerateLesson(APIView):
    """
    View that generates a lesson.
    All cards with battery levels below 4 (or repeating)
    are asked everyday.
    If a user have never seen a card, which means
    the user has no battery corresponding to the card
    the function will generate an introductory task.
    Options:
        ripeOnly - return only cards that were last updated
    only 1, 2, 7, 14 days ago depending on battery level
    """

    @staticmethod
    def _shuffle_examples(examples, size):
        if size > len(examples):
            size = len(examples)
        examples_serializer = ExamplesSerializer(examples, many=True)
        shuffled_raw = [ordered_dict["string"]
                        for ordered_dict in examples_serializer.data]
        shuffled = sample(shuffled_raw, size)
        return shuffled

    @staticmethod
    def _get_meanings(card, language_code):
        meanings = Meaning.objects.filter(
            card=card, language_code=language_code)
        meanings_serializer = MeaningSerializer(meanings, many=True)
        return meanings_serializer.data

    def get(self, request, pk):
        # Use's object and its additional fields
        user = request.user
        language_code = get_language_code(user)
        # Finding lesson by given ID
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"detail": "Lesson not found"}, status=404)
        # Maximal number of tasks needed for the client
        # TODO: add feature to set preferred max_tasks by default
        DEFAULT_MAX_TASKS = 7
        if "max_tasks" in request.query_params:
            try:
                max_tasks = int(request.query_params["max_tasks"])
            except ValueError:
                max_tasks = DEFAULT_MAX_TASKS
        else:
            max_tasks = DEFAULT_MAX_TASKS
        # Array where we will store generated tasks
        tasks = []
        for card in lesson.cards.all():
            # Stop generating tasks if max_tasks reached
            if len(tasks) >= max_tasks:
                break
            try:
                battery = card.batteries.get(user=user)
                level = battery.level
            except Battery.DoesNotExist:
                # Introduce the card to the user
                level = 0
            # -1 stands for BURIED cards
            if level == -1:
                continue
            examples = Example.objects.filter(string__icontains=card.word)
            # gender guessing task
            task = {
                "card_id": card.id,
                "word": card.word,
                "meanings": self._get_meanings(card, language_code),
                "examples": self._shuffle_examples(examples, 5),
                "answer": card.gender,
                "level": level
            }
            tasks.append(task)
        return Response(tasks)