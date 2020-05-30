from json import loads
from django.test import TestCase, Client
from django.contrib.auth.models import *
from main.models import *
from example.models import Example


class LessonsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("maria", password="123")
        self.token = Client().post("/api/login/", {"username": "maria", "password": "123"}).json()
        self.lesson = Lesson.objects.create(name="Lesson 1", difficulty="J")
        card = Card.objects.create(word="Test", gender="M", lesson=self.lesson)
        for i in range(5):
            Example.objects.create(string="Test {}".format(i + 1))
    
    def test_list_lessons(self):
        response = Client().get("/api/lessons/", HTTP_AUTHORIZATION="Bearer " + self.token["access"])
        self.assertEqual(len(response.json()), 1)

    def test_generate_lesson(self):
        response = Client().get(
            "/api/lessons/{}/".format(self.lesson.id),
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        response_parsed = response.json()
        self.assertEqual(len(response_parsed), 1)
