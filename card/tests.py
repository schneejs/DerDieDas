from json import loads

from django.contrib.auth.models import *
from django.test import Client, TestCase

from battery.models import Battery
from card.models import Card, Meaning
from example.models import Example
from lesson.models import Lesson


class CreateCardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("maria", password="123")
        self.token = Client().post(
            "/api/login/", {"username": "maria", "password": "123"}).json()
        self.headers = {
            'HTTP_AUTHORIZATION': "Bearer " + self.token["access"]
        }
        self.lesson = Lesson.objects.create(name="Lesson 1", difficulty="J")

    def test_add_card(self):
        response = Client().post("/api/card/create", {
            "lesson": self.lesson.id,
            "word": "Test",
            "gender": "F",
            "second_gender": "M"
        }, **self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(self.lesson.cards.all()), 1)

    def test_no_lesson_id(self):
        response = Client().post("/api/card/create", {
            "word": "Test",
            "gender": "F",
            "second_gender": "M"
        }, **self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(self.lesson.cards.all()), 0)

    def test_empty_word(self):
        response = Client().post("/api/card/create", {
            "lesson": self.lesson.id,
            "word": "",
            "gender": "F",
            "second_gender": "M"
        }, **self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(self.lesson.cards.all()), 0)

    def test_no_gender(self):
        response = Client().post("/api/card/create", {
            "lesson": self.lesson.id,
            "word": "",
            "gender": "",
            "second_gender": "M"
        }, **self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(self.lesson.cards.all()), 0)

    def test_wrong_gender(self):
        response = Client().post("/api/card/create", {
            "lesson": self.lesson.id,
            "word": "",
            "gender": "L",
            "second_gender": "M"
        }, **self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(self.lesson.cards.all()), 0)

    def test_second_gender_wrong(self):
        response = Client().post("/api/card/create", {
            "lesson": self.lesson.id,
            "word": "",
            "gender": "F",
            "second_gender": "L"
        }, **self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(self.lesson.cards.all()), 0)


class Meanings(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("maria", password="123")
        self.token = Client().post(
            "/api/login/", {"username": "maria", "password": "123"}).json()
        self.headers = {
            'HTTP_AUTHORIZATION': "Bearer " + self.token["access"]
        }
        self.lesson = Lesson.objects.create(name="Lesson 1", difficulty="J")
        self.intro_card = Card.objects.create(
            word="Test", gender="M", lesson=self.lesson)
        self.regular_card = Card.objects.create(
            word="Wort", gender="N", lesson=self.lesson)
        Meaning.objects.create(
            card=self.intro_card,
            language_code="en",
            meaning="Test meaning"
        )

    def test_empty_card(self):
        response = Client().get("/api/card/meanings/" +
                                str(self.regular_card.id), **self.headers)
        self.assertEqual(len(response.json()), 0)

    def test_full_card(self):
        response = Client().get("/api/card/meanings/" +
                                str(self.intro_card.id), **self.headers)
        self.assertEqual(len(response.json()), 1)

    def test_all_cards(self):
        response = Client().get("/api/card/meanings", **self.headers)
        self.assertEqual(len(response.json()), 1)

    def test_card_id_required(self):
        response = Client().post(
            "/api/card/meanings",
            {
                "card_id": "BEPISBEPIS",
                "language_code": "en",
                "meaning": "Word meaning"
            },
            **self.headers
        )
        self.assertEqual(response.status_code, 400)

    def test_language_code_does_not_exist(self):
        response = Client().post(
            "/api/card/meanings",
            {
                "card_id": self.regular_card.id,
                "language_code": "IDONTEXIST",
                "meaning": "Word meaning"
            },
            **self.headers
        )
        self.assertEqual(response.status_code, 400)

    def test_language_no_meaning_given(self):
        response = Client().post(
            "/api/card/meanings",
            {
                "card_id": self.regular_card.id,
                "language_code": "en",
            },
            **self.headers
        )
        self.assertEqual(response.status_code, 400)

    def test_adding_cards(self):
        response = Client().post(
            "/api/card/meanings",
            {
                "card_id": self.regular_card.id,
                "language_code": "en",
                "meaning": "Word meaning"
            },
            **self.headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["order"], 0)
        self.assertEqual(response.json()["meaning"], "Word meaning")


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

    def test_lessons_cards(self):
        headers = {
            'HTTP_AUTHORIZATION': "Bearer " + self.token["access"]
        }
        response = Client().get('/api/card/lesson/{}'.format(self.lesson.id), **headers)
        self.assertEqual(len(response.json()), 2)

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
