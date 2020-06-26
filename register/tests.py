from django.test import Client, TestCase


class TestRegister(TestCase):
    def test_languages(self):
        response = Client().get("/api/register/languages")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data), dict)

    def test_register_casual(self):
        response = Client().post("/api/register", {
            "username": "maria",
            "password": "sekret",
            "email": "maria@example.com",
            "first_name": "Maria",
            "last_name": "Müller"
        })
        self.assertEqual(response.status_code, 201)

    def test_register_wrong_username(self):
        response = Client().post("/api/register", {
            "username": "mari",
            "password": "sekret",
            "email": "maria@example.com",
            "first_name": "Maria",
            "last_name": "Müller"
        })
        self.assertEqual(response.status_code, 400)
        response = Client().post("/api/register", {
            "username": "mariа",  # last letter is cyrillic
            "password": "sekret",
            "email": "maria@example.com",
            "first_name": "Maria",
            "last_name": "Müller"
        })
        self.assertEqual(response.status_code, 400)

    def test_register_wrong_email(self):
        response = Client().post("/api/register", {
            "username": "maria",
            "password": "sekret",
            "email": "maria@examplecom",
            "first_name": "Maria",
            "last_name": "Müller"
        })
        self.assertEqual(response.status_code, 400)
        response = Client().post("/api/register", {
            "username": "maria",
            "password": "sekret",
            "email": "mariaexample.com",
            "first_name": "Maria",
            "last_name": "Müller"
        })
        self.assertEqual(response.status_code, 400)
