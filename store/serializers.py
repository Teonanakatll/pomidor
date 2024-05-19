from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation


# Роль сериализатора: конвертирование произвольных обьектов языка python в формат json, в том числе обьекты моделей
# и кверисеты, и наоборои из json в соответствующие обьекты языка python

class BooksSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        # id юзера возьмём из request.user
        fields = ('book', 'like', 'in_bookmarks', 'rate', 'favorite')