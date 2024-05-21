from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint


class Book(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    author_name = models.CharField(max_length=255, verbose_name='Имя Автора')
    discount = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Скидка')
    # создаём поле owner для того чтобы понимоть кто автор запсис
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_books', verbose_name='Автор')
    # явно связываем отношение ManyToMany через нашу таблицу, чтобы добавить в неё дополнительные поля
    # так как у нас дво поля связанны с User, возникает конфликт при обращении от юзера к книгам,
    # user.book (то ли прочитал, то ли написал), для этого прописываем related_name, по умолчанию related_name=book_set()
    # на к двум полям нельзя применить одинаковое название, для одной из связей нужно изменить название на своё
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='my_readers', verbose_name='Прочитанные книги')


    def __str__(self):
        return f"Id {self.id}: {self.name}"

class UserBookRelation(models.Model):
    # проверки и условия при создании связи ManyToMany:
    # CheckConstraint - Объект Q или булево Expression, который определяет проверку, которую вы хотите, чтобы ограничение выполняло.
    # CheckConstraint(check=Q(age__gte=18), name='age_gte_18') гарантирует, что поле возраст никогда не будет меньше 18.
    # UniqueConstrain - Список имен полей, определяющий уникальный набор столбцов, на которые необходимо наложить ограничение.
    # UniqueConstraint(fields=['room', 'date'], name='unique_booking') гарантирует, что каждый номер может быть забронирован
    # только один раз на каждую дату.
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    like = models.BooleanField(default=False, verbose_name='Лайки')
    favorite = models.BooleanField(default=False, verbose_name='Любимая книга')
    in_bookmarks = models.BooleanField(default=False, verbose_name='В закладках')
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, verbose_name='Рейтинг', null=True)

    def __str__(self):
        return f"{self.user}: {self.book.name}, RATE {self.rate}"

    class Meta:
        # ограничения для связи ManyToMany: не может существовоть двух записей с одинаковыми значениями полей
        constraints = [UniqueConstraint(fields=['user', 'book'], name='unique-like')]

