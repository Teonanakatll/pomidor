import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    # функция запускается каждый раз перед каждым тестом
    def setUp(self):
        # создаём юзера для добавления и изменения записей
        self.user = User.objects.create(username='test_username')

        # для всех манипуляций с обьектами нужно быть авторизованным
        self.client.force_login(self.user)

        self.book_1 = Book.objects.create(name='Test Boooook 1', price=250, author_name='Author 1')
        self.book_2 = Book.objects.create(name='Test Boooook 2', price=750, author_name='Author 3')
        self.book_3 = Book.objects.create(name='Test Boooook Author 1', price=550, author_name='Author 2')

    def test_get_list(self):
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

    def test_get_detail(self):
        url = reverse('book-detail', args=(self.book_2.id,))
        print(url)
        # client - клиентский запрос по апи адресу
        response = self.client.get(url)
        # print(response.data)
        # отправляем в сериализатор модели, data - чтобы получить сераализованные данные
        serializer_data = BooksSerializer(self.book_2).data
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

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        book_name = "For Whom The Bell Tools"
        data = {
            "name": book_name,
            "price": "1000.00",
            "author_name": "author"
        }
        # преобразуем данные в json для отправки
        json_data = json.dumps(data)

        response = self.client.post(url, data=json_data, content_type='application/json')

        new_book = BooksSerializer(Book.objects.get(name=book_name)).data
        # print(new_book)
        # print(response.data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # проверим что книг в базе столо 4
        self.assertEqual(4, Book.objects.all().count())
        # проверим заполнение полей
        self.assertEqual(new_book, response.data)

    def test_update(self):
        # с помощю args передаём в url id книги которую хотим изменить
        url = reverse('book-detail', args=(self.book_1.id,))
        # переменная для нового значения
        book_price = 3000
        data = {
            "name": self.book_1.name,
            "price": book_price,
            "author_name": self.book_1.author_name
        }
        # преобразуем данные в json для отправки
        json_data = json.dumps(data)

        response = self.client.put(url, data=json_data, content_type='application/json')

        # new_book = BooksSerializer(Book.objects.get(id=self.book_1.id)).data
        # print(new_book)
        # print(response.data)

        # обновляем переменную данными иэ дб
        self.book_1.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # проверим заполнение полей
        # self.assertEqual(book_price, Book.objects.get(id=self.book_1.id).price)
        self.assertEqual(book_price, self.book_1.price)

    def test_delete(self):
        # с помощю args передаём в url id книги которую хотим удалить
        url = reverse('book-detail', args=(self.book_3.id,))

        response = self.client.delete(url)

        delete_book = Book.objects.filter(id=self.book_3.id).exists()
        print(delete_book)
        # print(response.data)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        # проверим заполнение полей
        # self.assertEqual(book_price, Book.objects.get(id=self.book_1.id).price)
        self.assertEqual(False, delete_book)