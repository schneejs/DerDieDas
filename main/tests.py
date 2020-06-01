from json import loads

from django.contrib.auth.models import *
from django.test import Client, TestCase

from battery.models import Battery
from example.models import Example
from main.models import *


class LessonsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("maria", password="123")
        self.token = Client().post(
            "/api/login/", {"username": "maria", "password": "123"}).json()
        self.lesson = Lesson.objects.create(name="Lesson 1", difficulty="J")
        card1 = Card.objects.create(
            word="Test", gender="M", lesson=self.lesson)
        card2 = Card.objects.create(
            word="Wort", gender="N", lesson=self.lesson)
        Battery.objects.create(card=card2, user=self.user, level=0)
        Meaning.objects.create(
            card=card1,
            language_code="en",
            meaning="Test meaning"
        )
        for i in range(5):
            Example.objects.create(string="Test {}".format(i + 1))

    def test_list_lessons(self):
        response = Client().get(
            "/api/lessons/", HTTP_AUTHORIZATION="Bearer " + self.token["access"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_generate_lesson(self):
        response = Client().get(
            "/api/lessons/generate/{}/".format(self.lesson.id),
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        response_parsed = response.json()
        print(response_parsed)
        self.assertEqual(len(response_parsed), 2)

    def test_generate_lesson_with_max_one(self):
        response = Client().get(
            "/api/lessons/generate/{}/".format(self.lesson.id),
            {"max_tasks": 1},
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        response_parsed = response.json()
        self.assertEqual(len(response_parsed), 1)
