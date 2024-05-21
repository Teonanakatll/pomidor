import json

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, When, Case, Avg, F
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.generics import get_object_or_404
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    # функция запускается каждый раз перед каждым тестом
    def setUp(self):
        # создаём юзера для добавления и изменения записей
        self.user = User.objects.create(username='test_username')

        self.book_1 = Book.objects.create(name='Test Boooook 1', price=250, author_name='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Test Boooook 2', price=750, author_name='Author 3', owner=self.user)
        self.book_3 = Book.objects.create(name='Test Boooook Author 1', price=550, author_name='Author 2', owner=self.user)

        self.relation1 = UserBookRelation.objects.create(user=self.user, book=self.book_1, rate=5, like=True)

    def test_get_list(self):
        url = reverse('book-list')
        # print(url)
        # тестируем select_related() u prefetch_related в connection отлавливаем query-запросы
        with CaptureQueriesContext(connection) as queries:
            # client - клиентский запрос по апи адресу
            response = self.client.get(url)
        self.assertEqual(2, len(queries))
        # сериализатор отправляет кверисет с анотированным полем, поэтому дабавим его
        books = Book.objects.all().annotate(annotated_likes=
                                           Count(Case(When(userbookrelation__like=True, then=1))),
                                           rating=Avg('userbookrelation__rate'),
                                           price_with_discount=(F('price')-(F('price') / 100) * F('discount'))).order_by('id')
        # print(response.data)
        # отправляем в сериализатор модели, data - чтобы получить сераализованные данные
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['rating'], '5.00')
        # self.assertEqual(serializer_data[0]['likes_count'], 1)
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)
        # print(serializer_data)
        # print(response.data)

    def test_get_detail(self):
        url = reverse('book-detail', args=(self.book_2.id,))
        # print(url)
        # client - клиентский запрос по апи адресу
        response = self.client.get(url)
        # print(response.data)
        # сериализатор отправляет кверисет с анотированным полем, поэтому дабавим его
        books = Book.objects.filter(id=self.book_2.id).annotate(annotated_likes=
                                                                Count(Case(When(userbookrelation__like=True, then=1))),
                                                                rating=Avg('userbookrelation__rate'),
                                                                price_with_discount=(F('price')-(F('price') / 100) * F('discount'))).order_by('id')
        book = books[0]
        # отправляем в сериализатор модели, data - чтобы получить сераализованные данные
        serializer_data = BooksSerializer(book, many=False).data
        # print(serializer_data)
        # print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)



    def test_get_search(self):
        url = reverse('book-list')
        # print(url)
        # client - клиентский запрос но апи, передаём get-запросом словарь с запросом на поисе
        response = self.client.get(url, data={'search': 'Author 1'})
        # сериализатор отправляет кверисет с анотированными полями, поэтому дабавим их
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(annotated_likes=
                                           Count(Case(When(userbookrelation__like=True, then=1))),
                                           rating=Avg('userbookrelation__rate'),
                                           price_with_discount=(F('price')-(F('price') / 100) * F('discount'))).order_by('id')
        # отправляем в сериализатор модели, data - чтобы получить данные
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


    def test_get_ordering(self):
        url = reverse('book-list')
        # print(url)
        # client - клиентский запрос но апи, передаём get-запросом словарь с запросом на поисе
        response = self.client.get(url, data={'ordering': 'price'})
        # сериализатор отправляет кверисет с анотированными полями, поэтому дабавим их
        books = Book.objects.all().annotate(annotated_likes=
                                           Count(Case(When(userbookrelation__like=True, then=1))),
                                           rating=Avg('userbookrelation__rate'),
                                           price_with_discount=(F('price')-(F('price') / 100) * F('discount')))

        books = [books[0], books[2], books[1]]
        # отправляем в сериализатор модели, data - чтобы получить данные
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        # print(url)
        # client - клиентский запрос но апи, передаём get-запросом словарь с запросом на поисе
        response = self.client.get(url, data={'price': '750'})
        # сериализатор отправляет кверисет с анотированными полями, поэтому дабавим их
        books = Book.objects.filter(id=self.book_2.id).annotate(annotated_likes=
                                           Count(Case(When(userbookrelation__like=True, then=1))),
                                           rating=Avg('userbookrelation__rate'),
                                           price_with_discount=(F('price')-(F('price') / 100) * F('discount')))
        # отправляем в сериализатор модели, data - чтобы получить данные
        serializer_data = BooksSerializer(books, many=True).data
        # print(serializer_data)
        # print(response.data)
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

        # для всех манипуляций с обьектами нужно быть авторизованным
        self.client.force_login(self.user)

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
        # для всех манипуляций с обьектами нужно быть авторизованным
        self.client.force_login(self.user)

        response = self.client.put(url, data=json_data, content_type='application/json')

        # new_book = BooksSerializer(Book.objects.get(id=self.book_1.id)).data
        # print(new_book)
        # print('Data:', response.data)

        # обновляем переменную данными иэ дб
        self.book_1.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # проверим заполнение полей
        # self.assertEqual(book_price, Book.objects.get(id=self.book_1.id).price)
        self.assertEqual(book_price, self.book_1.price)

    # негативный тест (на безопасность), проверим perrmission class IsOwnerOrReadOnly пытаемся обновить запись не овнером
    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='not_owner')
        # логинимся под вторым юзером
        self.client.force_login(self.user2)

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

        self.assertEqual({'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.'
                                                , code='permission_denied')}, response.data)

        # обновляем переменную данными иэ дб
        self.book_1.refresh_from_db()

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        # проверим что цена не изменилась
        self.assertEqual(250, self.book_1.price)

    def test_update_not_owner_but_staff(self):
        # создаём юзера персонала
        self.user2 = User.objects.create(username='staff', is_staff=True)
        # логинимся под вторым юзером
        self.client.force_login(self.user2)
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

        # обновляем переменную данными иэ дб
        self.book_1.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # проверим что цена не изменилась
        self.assertEqual(3000, self.book_1.price)

    # негативный тест delete, удаление не под owner
    def test_delete(self):
        # с помощю args передаём в url id книги которую хотим удалить
        url = reverse('book-detail', args=(self.book_3.id,))

        # для всех манипуляций с обьектами нужно быть авторизованным
        self.client.force_login(self.user)

        response = self.client.delete(url)

        delete_book = Book.objects.filter(id=self.book_3.id).exists()
        # print(delete_book)
        # print(response.data)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        # проверим заполнение полей
        # self.assertEqual(book_price, Book.objects.get(id=self.book_1.id).price)
        self.assertEqual(False, delete_book)

    def test_delete_not_owner(self):
        self.user2 = User.objects.create(username='not_owner')
        self.client.force_login(self.user2)
        # с помощю args передаём в url id книги которую хотим удалить
        url = reverse('book-detail', args=(self.book_3.id,))

        response = self.client.delete(url)
        # print(response.status_code)

        delete_book = Book.objects.filter(id=self.book_3.id).exists()
        # print(delete_book)
        # print(response.data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        # проверим что запись существует
        self.assertEqual(True, delete_book)


class BooksRelationTestCase(APITestCase):
    # функция запускается каждый раз перед каждым тестом
    def setUp(self):
        # создаём юзера для добавления и изменения записей
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')

        # для всех манипуляций с обьектами нужно быть авторизованным
        self.client.force_login(self.user)

        self.book_1 = Book.objects.create(name='Test Boooook 1', price=250, author_name='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Test Boooook 2', price=750, author_name='Author 3', owner=self.user)

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        # print(url)

        data = {
            'like': True,
        }

        json_data = json.dumps(data)

        # метод patch такой-же как и put, только методом patch можно передавать несколько полей, при put все
        # например передать только лайк

        response = self.client.patch(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        # проверяем что лайк стоит
        self.assertTrue(relation.like)

        data = {
            'in_bookmarks': True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            'rate': 3,
        }
        json_data = json.dumps(data)
        # метод patch такой-же как и put, только методом patch можно передавать несколько полей, при put все
        # например передать только лайк

        response = self.client.patch(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        # проверяем что лайк стоит
        self.assertEqual(3, relation.rate)

    def test_rate_wrong(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            'rate': 6,
        }
        json_data = json.dumps(data)
        # метод patch такой-же как и put, только методом patch можно передавать несколько полей, при put все
        # например передать только лайк

        response = self.client.patch(url, data=json_data, content_type='application/json')
        # выводим response.data при неудачном сравнении
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        # проверяем что лайк стоит
        self.assertEqual(None, relation.rate)

    def test_favorite(self):
        # формируем url и добавляем в него позиционным параметром id книги
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        # создаём данные котрые хотим передать
        data = {
            'favorite': True,
        }
        # переводим их в формат json
        json_data = json.dumps(data)

        # отправляем клиент patch запрос на сформ url с json данными, одбавляем параметр content_type=applications/json
        response = self.client.patch(url, data=json_data, content_type='application/json')
        # проверяем статус ответа сервера
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # достаём обьект из бд
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        # print('relation', relation)
        # проверим что связь добавлена
        self.assertEqual(True, relation.favorite, response.data)


