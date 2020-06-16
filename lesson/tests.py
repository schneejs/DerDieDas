from json import loads

from django.contrib.auth.models import *
from django.test import Client, TestCase
from rest_framework.test import APIClient

from battery.models import Battery
from card.models import Card, Meaning
from example.models import Example
from lesson.models import Lesson


class LessonsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("maria", password="123")
        group = Group.objects.create(name="Editors")
        group.permissions.add(
            *[a.id for a in Permission.objects.filter(codename__contains="lesson")])
        group.permissions.add(
            *[a.id for a in Permission.objects.filter(codename__contains="card")])
        group.permissions.add(
            *[a.id for a in Permission.objects.filter(codename__contains="meaning")])
        group.permissions.add(
            *[a.id for a in Permission.objects.filter(codename__contains="example")])
        group.user_set.add(self.user)
        self.token = Client().post(
            "/api/login/", {"username": "maria", "password": "123"}).json()
        self.lesson = Lesson.objects.create(name="Lesson 1", difficulty="J")
        self.intro_card = Card.objects.create(
            word="Test", gender="M", lesson=self.lesson)
        self.regular_card = Card.objects.create(
            word="Wort", gender="N", lesson=self.lesson)
        Battery.objects.create(card=self.regular_card, user=self.user, level=0)
        Meaning.objects.create(
            card=self.intro_card,
            language_code="en",
            meaning="Test meaning"
        )
        for i in range(5):
            Example.objects.create(string="Test {}".format(i + 1))

    def test_create_delete_lesson(self):
        # Testing incorrect input
        response = Client().post("/api/lessons/create", {
            "name": "Lesson 2"  # has no difficulty
        }, HTTP_AUTHORIZATION="Bearer " + self.token["access"])
        self.assertEqual(response.status_code, 400)
        response = Client().post("/api/lessons/create", {
            "difficulty": 'M'
        }, HTTP_AUTHORIZATION="Bearer " + self.token["access"])
        self.assertEqual(response.status_code, 400)

        response = Client().post("/api/lessons/create", {
            "name": "Lesson 2",
            "difficulty": 'M'
        }, HTTP_AUTHORIZATION="Bearer " + self.token["access"])
        rjson = response.json()
        id = rjson["id"]
        self.assertGreater(id, 0)

        response = Client().get(
            "/api/lessons/list", HTTP_AUTHORIZATION="Bearer " + self.token["access"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        # Let's delete it
        response = Client().delete("/api/lessons/delete/{}".format(id),
                                   HTTP_AUTHORIZATION="Bearer " + self.token["access"])
        self.assertEqual(response.status_code, 200)

        # The number must decrease
        response = Client().get(
            "/api/lessons/list", HTTP_AUTHORIZATION="Bearer " + self.token["access"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_update_lesson(self):
        response = APIClient().patch(
            "/api/lessons/update/{}".format(self.lesson.id), 
            {
                "difficulty": 'M'
            },
            HTTP_AUTHORIZATION="Bearer " + self.token["access"],
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["difficulty"], 'M')

    def test_list_lessons(self):
        response = Client().get(
            "/api/lessons/list", HTTP_AUTHORIZATION="Bearer " + self.token["access"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_generate_lesson(self):
        response = Client().get(
            "/api/lessons/generate/{}".format(self.lesson.id),
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        response_parsed = response.json()
        self.assertEqual(len(response_parsed), 2)

    def test_generate_lesson_with_max_one(self):
        response = Client().get(
            "/api/lessons/generate/{}".format(self.lesson.id),
            {"max_tasks": 1},
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        response_parsed = response.json()
        self.assertEqual(len(response_parsed), 1)
