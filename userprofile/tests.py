from json import dumps

from django.contrib.auth.models import *
from django.test import Client, TestCase


class LessonsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("maria", password="123")
        self.user2 = User.objects.create_user("john", password="123")
        self.token = Client().post(
            "/api/login/", {"username": "maria", "password": "123"}).json()

    def test_user(self):
        response = Client().get(
            "/api/profile/maria",
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        obj = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(obj["id"], 1)

    def test_user_no_username(self):
        response = Client().get(
            "/api/profile/",
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        obj = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(obj["id"], 1)

    def test_nonexistent(self):
        response = Client().get(
            "/api/profile/doesntexist",
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        self.assertEqual(response.status_code, 404)

    def test_set_language(self):
        response = Client().patch(
            "/api/profile/maria",
            {"language_code": "ru"},
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.languagecode.language_code, "ru")

    def test_set_language_protected(self):
        """
        We're trying to change user john's field
        with maria's token, that will fail
        """
        response = Client().patch(
            "/api/profile/john",
            {"language_code": "ru"},
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        with self.assertRaises(User.languagecode.RelatedObjectDoesNotExist):
            self.user2.languagecode.language_code
        self.assertEqual(response.status_code, 403)

    def test_put_method_fails(self):
        response = Client().put(
            "/api/profile/maria",
            {"username": "irina", "language_code": "ru"},
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        self.assertEqual(response.status_code, 405)
