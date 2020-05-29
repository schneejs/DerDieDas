from json import loads
from django.test import TestCase, Client
from django.contrib.auth.models import *
from main.models import *


class LessonsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("maria", password="123")
        self.token = Client().post("/api/login/", {"username": "maria", "password": "123"}).json()
        for i in range(10):
            Lesson.objects.create(name="Lesson {}".format(i), difficulty="J")
    
    def test_list_lessons(self):
        response = Client().get("/api/lessons/", HTTP_AUTHORIZATION="Bearer " + self.token["access"])
        self.assertEqual(len(response.json()), 10)

    def test_view_lesson(self):
        response = Client().get("/api/lessons/1/", HTTP_AUTHORIZATION="Bearer " + self.token["access"])
        response_parsed = response.json()
        self.assertEqual(response_parsed["name"], "Lesson 0")
