from django.test import TestCase
from django.urls import reverse


class BookTestCase(TestCase):
    def test_book_list_page_returns_200(self):
        url = reverse("book_list_open")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
