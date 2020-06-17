from enum import IntEnum
from math import expm1
from random import choice, random, sample

from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView)
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


class ListLessons(ListAPIView):
    """
    View for listing public lessons
    """
    queryset = Lesson.objects.filter(is_public=True)
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class ListAllLessons(ListAPIView):
    """
    View for listing all lessons. Useful for editors.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsEditor]


class CreateLesson(CreateAPIView):
    """
    View for creating lessons for editors
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsEditor]


class DeleteLesson(DestroyAPIView):
    """
    View for deleting lessons for editors
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsEditor]

    def destroy(self, request, pk=None):
        lesson = get_object_or_404(Lesson, pk=pk)
        lesson.cards.all().delete()
        lesson.delete()
        return Response()


class UpdateLesson(UpdateAPIView):
    """
    View for updating lessons
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsEditor]


class GenerateLesson(APIView):
    """
    View that generates a lesson.
    All cards with battery levels below 4 (or repeating)
    are asked everyday.
    If a user have never seen a card, which means
    the user has no battery corresponding to the card
    the function will generate an introductory task.
    Options:
        ripe-only [1, 0] - return only cards that were last updated
    only 1, 2, 7, 14 days ago depending on battery level,
    defaults to true.
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

    @staticmethod
    def _is_ripe(dt, level):
        return dt.now().timestamp() - dt.timestamp() > expm1(level) * 86400

    def get(self, request, pk):
        # Parameters
        try:
            ripe_only = request.query_params["ripe-only"] == '1'
        except:
            # if something goes wrong use this default value
            ripe_only = True
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
                # Skip generating this task if not enough time
                # passed from last update
                # we don't need it if battery doesn't exist
                if ripe_only and not self._is_ripe(battery.last_modified, level):
                    continue
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
                "answer": card.gender if card.second_gender is None else card.gender + card.second_gender,
                "level": level
            }
            tasks.append(task)
        return Response(tasks)
