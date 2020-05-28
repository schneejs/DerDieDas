from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from json import loads
from main.models import *
from battery.models import *


class BatteryTest(TestCase):
    def setUp(self):
        self.users = [
            User.objects.create_user("maria", password="123"),
            User.objects.create_user("alice", password="123")
        ]
        self.lessons = [
            Lesson.objects.create(name="Tiere", difficulty="J"),
            Lesson.objects.create(name="Werkzeuge", difficulty="M")
        ]
        cards = [
            Card.objects.create(lesson=self.lessons[0], word="Wolf", gender="M"),
            Card.objects.create(lesson=self.lessons[1], word="Axt", gender="F")
        ]
        for user in self.users:
            for card in cards:
                Battery.objects.create(user=user, card=card, level=1)
        self.tokens = []
        c = Client()
        for user in self.users:
            token = c.post("/api/login/", {"username": user.username, "password": "123"})
            self.tokens.append(token.json())
    
    def test_by_user(self):
        user = self.users[0]
        token = self.tokens[0]
        c = Client()
        auth_headers = {
            'HTTP_AUTHORIZATION': "Bearer " + token["access"]
        }
        response = c.get("/api/battery/", **auth_headers)
        response_json = loads(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), 2)
    
    def test_by_lesson(self):
        user = self.users[1]
        token = self.tokens[1]
        lesson = self.lessons[0]
        c = Client()
        auth_headers = {
            'HTTP_AUTHORIZATION': "Bearer " + token["access"]
        }
        response = c.get("/api/battery/", {'lesson_id': lesson.id}, **auth_headers)
        response_json = loads(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), 1)