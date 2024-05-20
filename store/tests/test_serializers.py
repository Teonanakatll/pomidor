from django.db.models import Count, Case, When, Avg, F
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(APITestCase):

    def setUp(self):
        # создаём юзера для добавления и изменения записей
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')

        # для всех манипуляций с обьектами нужно быть авторизованным
        # self.client.force_login(self.user)

        self.book_1 = Book.objects.create(name='Test Book 1', author_name='Author 1', price=250, discount=3)
        self.book_2 = Book.objects.create(name='Test Book 2', author_name='Author 2', price=550, discount=4)

        self.relation1 = UserBookRelation.objects.create(user=self.user1, book=self.book_1, rate=5, like=True)
        self.relation2 = UserBookRelation.objects.create(user=self.user2, book=self.book_1, rate=5, like=True)
        self.relation3 = UserBookRelation.objects.create(user=self.user3, book=self.book_1, rate=4, like=True)

        self.relation4 = UserBookRelation.objects.create(user=self.user1, book=self.book_2, rate=3, like=True)
        self.relation5 = UserBookRelation.objects.create(user=self.user2, book=self.book_2, rate=4, like=True)
        self.relation6 = UserBookRelation.objects.create(user=self.user3, book=self.book_2, like=False)


    def test_ok(self):
        # Case() используется для создания условных выражений в запросах к бд. Он позволяет выполнять sql-подобные
        # условия (как CASE в sql), когда нужно выполнить различные действия в зависимости от значения полей.
        # When() - указывает когда необходимо подсчитывать значения. then - в током случае возвращаем 1
        books = Book.objects.all().annotate(annotated_likes
                                            =Count(Case(When(userbookrelation__like=True, then=1))),
                                            rating=Avg('userbookrelation__rate'),
                                            price_with_discount=(F('price')-(F('price') / 100) * F('discount'))).order_by('id')
        data = BooksSerializer(books, many=True).data
        # print(data)
        expected_data = [
            {
                'id': self.book_1.id,
                'name': 'Test Book 1',
                'author_name': 'Author 1',
                'likes_count': 3,
                'annotated_likes': 3,
                'rating': '4.67',
                'price': '250.00',
                'discount': 3,
                'price_with_discount': '242.50'
            },
            {
                'id': self.book_2.id,
                'name': 'Test Book 2',
                'author_name': 'Author 2',
                'likes_count': 2,
                'annotated_likes': 2,
                'rating': '3.50',
                'price': '550.00',
                'discount': 4,
                'price_with_discount': '528.00'
            }
        ]
        print(data)

        self.assertEqual(expected_data, data)

