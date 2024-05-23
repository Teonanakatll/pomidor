from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation


# Роль сериализатора: конвертирование произвольных обьектов языка python в формат json, в том числе обьекты моделей
# и кверисеты, и наоборои из json в соответствующие обьекты языка python

# сериализатор для отображения вложенных полей модели User
class BookReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class BooksSerializer(ModelSerializer):
    # дописываем своё поле с методом, поле будет хранить аннатацию с подсчётом лайков к каждой книге
    # likes_count u annotated_likes две реализации одного и того же результата, N+1

    # соглашение об использавании имён SerializerMethodField с префиксом get_название переменной
    # price = serializers.SerializerMethodField()

    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    price_with_discount = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    # через ForeihnKey берём значение ownera
    # чтобы небыло N+1 во вью выбираем ownera через select_related
    owner_name = serializers.CharField(source='owner.username', default="", read_only=True)

    # добавляем поле которому присваиваем результат работы дпугого сериалайзера для добавления вложенных полей из связaнных записей
    # через связь ManyToMany (поле readers), поле должно называться как и поле в модели Book те readers
    # если хотим указать другое имя, то необходимо указать source='readers' в параметрах
    readers = BookReaderSerializer(many=True, read_only=True)

    # def get_price(self, instance):
    #     return (instance.price -
    #             instance.price * (instance.discount / 100))

    class Meta:
        model = Book
        fields = ('id', 'name', 'rating', 'author_name',
                  'annotated_likes', 'price', 'discount',
                  'price_with_discount', 'owner_name', 'readers')

    # добавляем свою функцию в созданный метод, эта также можно сделать с помощю анотации
    # self- сам сериализатор, instance - это книга которую мы в данный момент сериализуем
    # добовляет n+1
    # def get_likes_count(self, instance):
    #     # фильтруем записи UserBookRelation по текущей книге с like=True и считаем их количество
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        # id юзера возьмём из request.user
        fields = ('book', 'like', 'in_bookmarks', 'rate', 'favorite')