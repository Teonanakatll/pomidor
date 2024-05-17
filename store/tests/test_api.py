from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    # функция запускается каждый раз перед каждым тестом
    def setUp(self):
        self.book_1 = Book.objects.create(name='Test Boooook 1', price=250, author_name='Author 1')
        self.book_2 = Book.objects.create(name='Test Boooook 2', price=750, author_name='Author 3')
        self.book_3 = Book.objects.create(name='Test Boooook Author 1', price=550, author_name='Author 2')

    def test_get(self):
        url = reverse('book-list')
        print(url)
        # client - клиентский запрос по апи адресу
        response = self.client.get(url)
        # print(response.data)

        # отправляем в сериализатор модели, data - чтобы получить сераализованные данные
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        # print(serializer_data)
        # print(response.data)

    def test_get_search(self):
        url = reverse('book-list')
        print(url)
        # client - клиентский запрос но апи, передаём get-запросом словарь с запросом на поисе
        response = self.client.get(url, data={'search': 'Author 1'})

        # отправляем в сериализатор модели, data - чтобы получить данные
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


    def test_get_ordering(self):
        url = reverse('book-list')
        print(url)
        # client - клиентский запрос но апи, передаём get-запросом словарь с запросом на поисе
        response = self.client.get(url, data={'ordering': 'price'})

        # отправляем в сериализатор модели, data - чтобы получить данные
        serializer_data = BooksSerializer([self.book_1, self.book_3, self.book_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        print(url)
        # client - клиентский запрос но апи, передаём get-запросом словарь с запросом на поисе
        response = self.client.get(url, data={'price': '750'})

        # отправляем в сериализатор модели, data - чтобы получить данные
        serializer_data = BooksSerializer([self.book_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)