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
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)


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

    # В Python метод __init__ является конструктором класса. Этот метод вызывается автоматически при создании нового
    # объекта класса и используется для инициализации его атрибутов. Конструктор __init__ позволяет задавать начальные
    # значения переменных объекта и выполнять другие действия при создании экземпляра класса.
    # переопределяем метод __init__ модели
    def __init__(self, *args, **kwargs):
        # вызываем родительский метод super.__init__ чтобы он не перезаписался
        super(UserBookRelation, self).__init__(*args, **kwargs)
        # берём заначение поля rate до сохранения записи
        self.old_rating = self.rate

    # вызывается каждый раз после добавления или изменения модели
    def save(self, *args, **kwargs):

        # до момента вызова supre().save() родительского класса pk ещё не доступен
        creating = not self.pk

        super().save(*args, **kwargs)
        print('old_rating', self.old_rating)

        # и значение поля rate после сохранения
        new_rating = self.rate
        print('new_rating', new_rating)
        # from store.logic import set_rating
        #
        # set_rating(self.book)
        # и если они не равны или рейтинг добавляется первый раз, тогда обновляем рейтинг
        if self.old_rating != new_rating or creating:
            # делаем локальный импорт чтобы избежать перекрёстного импорта, (в фунцию set_rating() мы импортировали данный класс)
            from store.logic import set_rating
            # вызываем функцию обновления рейтинга
            set_rating(self.book)

    class Meta:
        # ограничения для связи ManyToMany: не может существовоть двух записей с одинаковыми значениями полей
        constraints = [UniqueConstraint(fields=['user', 'book'], name='unique-like')]

