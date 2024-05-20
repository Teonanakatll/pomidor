from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation


# Роль сериализатора: конвертирование произвольных обьектов языка python в формат json, в том числе обьекты моделей
# и кверисеты, и наоборои из json в соответствующие обьекты языка python

class BooksSerializer(ModelSerializer):
    # дописываем своё поле с методом, поле будет хранить аннатацию с подсчётом лайков к каждой книге
    # likes_count u annotated_likes две реализации одного и того же результата
    likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    price_with_discount = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    class Meta:
        model = Book
        fields = ('id', 'name', 'author_name', 'likes_count',
                  'annotated_likes', 'rating', 'price', 'discount', 'price_with_discount')

    # добавляем свою функцию в созданный метод, эта также можно сделать с помощю анотации
    # self- сам сериализатор, instance - это книга которую мы в данный момент сериализуем
    def get_likes_count(self, instance):
        # фильтруем записи UserBookRelation по текущей книге с like=True и считаем их количество
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        # id юзера возьмём из request.user
        fields = ('book', 'like', 'in_bookmarks', 'rate', 'favorite')