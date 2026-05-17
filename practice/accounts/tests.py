from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import *

User = get_user_model()


class BookTestCase(TestCase):
    def test_book_list_page_returns_200(self):
        url = reverse("book_list_open")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class AccountsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.url = reverse("test_open")

    def test_test_open_not_login(self):
        """
        1. 未ログイン状態のテスト
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_test_open_login(self):
        """
        2. ログイン状態のテスト
        """
        self.client.login(username="testuser", password="testpassword")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "test.html")

        self.assertEqual(response.context["page_title"], "勉強場1")

        self.assertIsInstance(response.context["input_form"], TestForm)
        self.assertIsInstance(response.context["select_form"], TestSelect)
        self.assertIsInstance(response.context["book_form"], BookForm)
