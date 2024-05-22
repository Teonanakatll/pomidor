# from unittest import result
from rest_framework.test import APITestCase
from django.test import TestCase


from django.contrib.auth.models import User

from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        # создаём юзера для добавления и изменения записей
        self.user1 = User.objects.create(username='user1', first_name='Fedor', last_name='Fundukov')
        self.user2 = User.objects.create(username='user2', first_name='Igor', last_name='Rubakov')
        self.user3 = User.objects.create(username='user3', first_name='Monya', last_name='Cherpakov')

        self.book_1 = Book.objects.create(name='Test Book 1', author_name='Author 1', price=250, discount=3, owner=self.user1)

        self.relation1 = UserBookRelation.objects.create(user=self.user1, book=self.book_1, rate=5, like=True)
        self.relation2 = UserBookRelation.objects.create(user=self.user2, book=self.book_1, rate=5, like=True)
        self.relation3 = UserBookRelation.objects.create(user=self.user3, book=self.book_1, rate=4, like=True)

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67', str(round(self.book_1.rating, 2)))