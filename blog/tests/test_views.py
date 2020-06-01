from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class IndexViewTest(TestCase):
    def test_redirect2blog(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 301)
        self.assertEqual('/' + response.url, reverse('index'))
