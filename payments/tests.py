from django.test import TestCase

class SimpleTest(TestCase):
    def test_homepage_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # редирект на логин
