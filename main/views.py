from random import random, sample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from main.models import Lesson
from battery.models import Battery
from example.models import Example
from main.serializers import LessonSerializer, LessonFullSerializer
from battery.serializers import BatterySerializer
from example.serializers import ExamplesSerializer


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
        shuffled_raw = [ordered_dict["string"] for ordered_dict in examples_serializer.data]
        shuffled = sample(shuffled_raw, size)
        return shuffled

    def get(self, request, pk):
        user = request.user
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"detail": "Lesson not found"}, status=404)
        tasks = []
        for card in lesson.cards.all():
            try:
                battery = card.batteries.get(user=user)
                level = battery.level
            except Battery.DoesNotExist:
                # Introduce the card to the user
                level = -1
            examples = Example.objects.filter(string__icontains=card.word)
            task = {"card_id": card.id}
            if level == -1:
                task["type"] = "intro"
                task["word"] = str(card)
                task["examples"] = self._shuffle_examples(examples, 5)
            elif level == 0:
                if random() < 0.5:
                    task["type"] = "gender"
                    task["word"] = card.word
                    task["gender"] = card.gender
                else:
                    task["type"] = "meaning"
                    task["word"] = str(card)
            elif level > 2:
                # TODO: 4th task type
                pass
            tasks.append(task)
        return Response(tasks)
            