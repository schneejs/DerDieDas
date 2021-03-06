from itertools import repeat
from json import dumps

from django.contrib.auth.models import *
from django.test import Client, TestCase


class LessonsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "maria", "test@example.com", "123")
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

    def test_set_long_first_name(self):
        response = Client().patch(
            "/api/profile/maria",
            {"first_name": "".join(repeat('a', 41))},
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        self.assertIn("detail", response.json())
        self.assertIn("first_name", response.json()["detail"])
        self.assertEqual(response.status_code, 400)

    def test_set_email(self):
        response = Client().get(
            "/api/profile/maria",
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        self.assertIn("email", response.json())
        self.assertEqual(response.json()["email"], "test@example.com")

        response = Client().patch(
            "/api/profile/maria",
            {"email": "newtest@example.com"},
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        response = Client().get(
            "/api/profile/maria",
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        self.assertIn("email", response.json())
        self.assertEqual(response.json()["email"], "newtest@example.com")

    def test_put_method_fails(self):
        response = Client().put(
            "/api/profile/maria",
            {"username": "irina", "language_code": "ru"},
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer " + self.token["access"]
        )
        self.assertEqual(response.status_code, 405)


class EditorsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("maria", password="123")
        self.user2 = User.objects.create_user("john", password="123")
        group = Group.objects.create(name="Editors")
        group.permissions.add(
            *[a.id for a in Permission.objects.filter(codename__contains="lesson")])
        group.permissions.add(
            *[a.id for a in Permission.objects.filter(codename__contains="card")])
        group.permissions.add(
            *[a.id for a in Permission.objects.filter(codename__contains="meaning")])
        group.permissions.add(
            *[a.id for a in Permission.objects.filter(codename__contains="example")])
        group.user_set.add(self.user2)
        self.editors = group
        self.token = Client().post(
            "/api/login/", {"username": "maria", "password": "123"}).json()
        self.token2 = Client().post(
            "/api/login/", {"username": "john", "password": "123"}).json()
        self.headers = {
            "HTTP_AUTHORIZATION": "Bearer " + self.token["access"]
        }
        self.headers2 = {
            "HTTP_AUTHORIZATION": "Bearer " + self.token2["access"]
        }

    def test_is_editor(self):
        response = Client().get("/api/profile/maria", **self.headers)
        rjson = response.json()
        self.assertEqual(rjson["is_editor"], False)

        response = Client().get("/api/profile/john", **self.headers)
        rjson = response.json()
        self.assertEqual(rjson["is_editor"], True)

    def test_create_lesson(self):
        # Must deny access
        response = Client().post("/api/lessons/create", {
            "name": "Test3",
            "difficulty": "M"
        }, **self.headers)
        self.assertEqual(response.status_code, 403)
        # Must grant access
        response = Client().post("/api/lessons/create", {
            "name": "Test3",
            "difficulty": "M"
        }, **self.headers2)
        self.assertEqual(response.status_code, 201)


class ChangePasswordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("maria", password="123")
        token = Client().post(
            "/api/login/", {"username": "maria", "password": "123"}).json()
        self.headers = {
            "HTTP_AUTHORIZATION": "Bearer " + token["access"]
        }

    def test_regular_change(self):
        response = Client().post("/api/profile/password/change", {
            "old_password": "123",
            "new_password": "456"
        }, **self.headers)
        self.assertEqual(response.status_code, 200)

        response = Client().post(
            "/api/login/", {"username": "maria", "password": "456"})
        self.assertEqual(response.status_code, 200)

        response = Client().post(
            "/api/login/", {"username": "maria", "password": "123"})
        self.assertEqual(response.status_code, 401)

    def test_no_old_password_given(self):
        response = Client().post("/api/profile/password/change", {
            "new_password": "456"
        }, **self.headers)
        self.assertEqual(response.status_code, 400)

        response = Client().post(
            "/api/login/", {"username": "maria", "password": "456"})
        self.assertEqual(response.status_code, 401)

        response = Client().post(
            "/api/login/", {"username": "maria", "password": "123"})
        self.assertEqual(response.status_code, 200)

    def test_no_new_password_given(self):
        response = Client().post("/api/profile/password/change", {
            "old_password": "123",
        }, **self.headers)
        self.assertEqual(response.status_code, 400)

        response = Client().post(
            "/api/login/", {"username": "maria", "password": "456"})
        self.assertEqual(response.status_code, 401)

        response = Client().post(
            "/api/login/", {"username": "maria", "password": "123"})
        self.assertEqual(response.status_code, 200)
