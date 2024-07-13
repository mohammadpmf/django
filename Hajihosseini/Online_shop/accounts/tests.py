from django.test import TestCase
from django.urls import reverse


class AccountsTest(TestCase):
    def test_get_login_page_by_url_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_get_signup_page_by_url_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_is_Log_In_Page_text_in_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'Log In Page')
    
    def test_is_Sign_Up_Page_text_in_signup_page(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'Sign Up Page')
        