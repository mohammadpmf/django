from django.test import TestCase
from django.urls import reverse


class PagesTests(TestCase):
    def test_get_home_page_by_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_get_home_page_by_url_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_get_about_us_page_by_url(self):
        response = self.client.get('/aboutus/')
        self.assertEqual(response.status_code, 200)

    def test_get_about_us_page_by_url_name(self):
        response = self.client.get(reverse('aboutus'))
        self.assertEqual(response.status_code, 200)
    
    
