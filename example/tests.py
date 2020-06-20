from django.test import TestCase, Client
from django.contrib.auth.models import User
from json import loads
from lesson.models import *
from example.models import *


class ExampleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("maria", password="123")
        c = Client()
        self.token = c.post("/api/login/", {"username": "maria", "password": "123"}).json()
        examples = [
            "I like Django",
            "The woman does not like potatoes",
            "The woman loves his career"
        ]
        for example in examples:
            Example.objects.create(string=example)
    
    def test_two_words(self):
        c = Client()
        headers = {
            'HTTP_AUTHORIZATION': "Bearer " + self.token["access"]
        }
        response_like = c.get("/api/examples/search/like", **headers)
        response_woman = c.get("/api/examples/search/woman", **headers)
        self.assertEqual(len(response_like.json()), 2)
        self.assertEqual(len(response_woman.json()), 2)