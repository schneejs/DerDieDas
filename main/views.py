from random import random, sample

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from battery.models import Battery
from battery.serializers import BatterySerializer
from example.models import Example
from example.serializers import ExamplesSerializer
from login.utils import get_language_code
from main.models import Lesson, Meaning
from main.serializers import LessonSerializer, MeaningSerializer


class ListLessons(ListAPIView):
    """
    View for listing lessons
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class GenerateLesson(APIView):
    """
    View that generates a lesson. It creates different tasks
    for the user according to their cards' batteries.
    Types of tasks:
        1. Word introduction. Creates a new battery.
        2. Guess the gender. Given three buttons with article
    names: der, die, das.
        3. Guess the meaning. Given four words and several
    examples, one of them is the correct answer.
        4. Analyze three examples. Given three examples of one
    hidden word, the user needs to find it.
    Correct answer charges the battery and vice versa.
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
        print(Meaning.objects.filter())
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
                level = -1
            examples = Example.objects.filter(string__icontains=card.word)
            task = {"card_id": card.id}
            if level == -1:
                # word introduction
                task["type"] = "intro"
                task["word"] = str(card)
                task["meanings"] = self._get_meanings(card, language_code)
                task["examples"] = self._shuffle_examples(examples, 5)
            elif level == 0:
                if random() < 0.5:
                    # gender guessing task
                    task["type"] = "gender"
                    task["word"] = card.word
                else:
                    # meaning guessing task
                    task["type"] = "meaning"
                    task["word"] = str(card)
            elif level > 2:
                # TODO: 4th task type
                pass
            tasks.append(task)
        return Response(tasks)
