from django.db.models import Avg

from store.models import UserBookRelation


def set_rating(book):
    # обращаемся к модели UserBookRelation и фильтруем записи по полю book (из переданного аргумента)
    # aggregate возвращает словарь из полей query которые мы указали внутри aggregate и тех значений которые мы присвоили
    # тоесть аггрегирует словарь с ключём и значением которое мы прописали в aggregate (агрегация колекции обьектов)
    # агрегируем новое поле
    rating = UserBookRelation.objects.filter(book=book).aggregate(rating=Avg('rate')).get('rating')
    # добавляем в поле rating переданной книги
    book.rating = rating

    book.save()
