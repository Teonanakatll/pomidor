import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from drf.models import Women


# Роль сериализатора: конвертирование произвольных обьектов языка python в формат json, в том числе обьекты моделей
# и кверисеты, и наоборои из json в соответствующие обьекты языка python


class WomenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Women
        # cat - записываем название поля внешнего ключа
        fields = "__all__"

# class WomenSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#     created = serializers.DateTimeField(read_only=True)
#     updated = serializers.DateTimeField(read_only=True)
#     is_published = serializers.BooleanField(default=True)
#     cat_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return Women.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get("title", instance.title)
#         instance.content = validated_data.get("content", instance.content)
#         instance.updated = validated_data.get("updated", instance.updated)
#         instance.is_published = validated_data.get("is_published", instance.is_published)
#         instance.cat_id = validated_data.get("cat_id", instance.cat_id)
#         instance.save()
#         return instance
#
#     def delete(self, instance):
#         instance.delete()
#         return instance.title


# class WomenModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content
#
#
# class WomenSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#
#
# def encode():
#     model = WomenModel('Angelina Joile', 'Goliwood actriss')
#     model_sr = WomenSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Angelina Joile","content":"Goliwood actriss"}')
#     data = JSONParser().parse(stream)
#     # чтобы декодировать данные нужно использовать именованный параметр data
#     serializer = WomenSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)