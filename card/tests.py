from json import loads

from django.contrib.auth.models import *
from django.test import Client, TestCase

from battery.models import Battery
from card.models import Card, Meaning
from example.models import Example
from lesson.models import Lesson


class BuriedCards(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("maria", password="123")
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

    def test_answer(self):
        headers = {
            'HTTP_AUTHORIZATION': "Bearer " + self.token["access"]
        }
        for _ in range(7):
            Client().post(
                "/api/card/answer/{}/1".format(self.intro_card.id),
                **headers
            )
            Client().post(
                "/api/card/answer/{}/0".format(self.regular_card.id),
                **headers
            )
        response = Client().get(
            "/api/lessons/generate/{}?ripe-only=0".format(self.lesson.id),
            **headers
        )
        response_parsed = response.json()
        self.assertEqual(response_parsed[0]["level"], 4)
        self.assertEqual(response_parsed[1]["level"], 0)

    def test_buries(self):
        headers = {
            'HTTP_AUTHORIZATION': "Bearer " + self.token["access"]
        }

        response = Client().post(
            "/api/card/bury/{}".format(self.intro_card.id),
            **headers
        )
        self.assertEqual(response.status_code, 200)

        response = Client().get(
            "/api/lessons/generate/{}".format(self.intro_card.id),
            **headers
        )
        self.assertEqual(len(response.json()), 1)

        response = Client().get(
            "/api/card/buried/lesson/{}".format(self.lesson.id),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        response = Client().get(
            "/api/card/buried",
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        # Create another lesson
        lesson2 = Lesson.objects.create(name="Test2", difficulty='J')
        new_card = Card.objects.create(
            lesson=lesson2, word="EINWORT", gender='F', second_gender='M')

        response = Client().post(
            "/api/card/bury/{}".format(new_card.id),
            **headers
        )
        self.assertEqual(response.status_code, 200)

        response = Client().get(
            "/api/card/buried/lesson/{}".format(self.lesson.id),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        response = Client().get(
            "/api/card/buried",
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        response = Client().post(
            "/api/card/unbury/{}".format(self.lesson.id),
            **headers
        )
        self.assertEqual(response.status_code, 200)

        response = Client().get(
            "/api/lessons/generate/{}".format(self.lesson.id),
            **headers
        )
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["level"], 0)
