from rest_framework.serializers import ModelSerializer

from store.models import Book


# Роль сериализатора: конвертирование произвольных обьектов языка python в формат json, в том числе обьекты моделей
# и кверисеты, и наоборои из json в соответствующие обьекты языка python

class BooksSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'