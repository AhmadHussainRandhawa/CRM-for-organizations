from django.test import TestCase
from django.shortcuts import reverse


class HomePageTest(TestCase):

    def test_get(self):
        self.client.login(username='AhmadHussain', password='LATITUDEE@')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

