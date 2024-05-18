from unittest import TestCase

from django.contrib.auth.models import User

from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):

        # создаём юзера для добавления и изменения записей
        self.user = User.objects.create(username='test_username')

        # для всех манипуляций с обьектами нужно быть авторизованным
        # self.client.force_login(self.user)

        book_1 = Book.objects.create(name='Test Book 1', author_name='Author 1', price=250, owner=self.user)
        book_2 = Book.objects.create(name='Test Book 2', author_name='Author 2', price=550, owner=self.user)

        data = BooksSerializer([book_1, book_2], many=True).data
        print(data)
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test Book 1',
                'price': '250.00',
                'author_name': 'Author 1',
                'owner': book_1.owner.id
            },
            {
                'id': book_2.id,
                'name': 'Test Book 2',
                'price': '550.00',
                'author_name': 'Author 2',
                'owner': book_2.owner.id
            }
        ]

        self.assertEqual(expected_data, data)