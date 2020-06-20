from django.test import Client, TestCase


class TestRegister(TestCase):
    def test_languages(self):
        response = Client().get("/api/register/languages")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data), dict)
