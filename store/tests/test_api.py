from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(name='Test Book 1', price=250)
        book_2 = Book.objects.create(name='Test Book 2', price=550)
        url = reverse('book-list')
        # client - клиентский запрос
        response = self.client.get(url)

        # data - чтобы получить данные
        serializer_data = BooksSerializer([book_1, book_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        print(response.status_code)
        print(response.data)