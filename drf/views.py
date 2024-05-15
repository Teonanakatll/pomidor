from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from drf.models import Women, Category
from drf.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from drf.serializers import WomenSerializer

# Ограничение доступа (permissions)
# AllowAny - полный доступ (стоит по умолчанию)
# isAuthenticated - только для зарегистрированных пользователей
# isAdminUser - только для администраторов
# isAuthenticatedOrReadOnly - только для авторизованных или всем, но только для чтения

class WomenAPIList(generics.ListCreateAPIView):
     queryset = Women.objects.all()
     serializer_class = WomenSerializer
     permission_classes = (IsAuthenticatedOrReadOnly, )


class WomenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class WomenAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    # IsAdminOrReadOnly - наш собственный класс
    permission_classes = (IsAdminOrReadOnly,)


# class WomenViewSet(viewsets.ModelViewSet):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#     # для получения пользователем выборки моделей необходимо переопределить метод get_queryset
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#
#         if not pk:
#             return Women.objects.all()[:3]
#
#         # метод filter возвращает список с одной записью, qet_queryset должен возвращать список
#         return Women.objects.filter(pk=pk)
#
#     # если стандартных путей недостаточно можно добавлять даполнительные с помощю декоратора @action(methods=['get'])
#     # detail=True - вернуть одну запись
#     @action(methods=['get'], detail=True)
#     def category(self, request, pk=None):
#         cats = Category.objects.get(pk=pk)
#         return Response({'cats': cats.name})

# # реаоизует 2 метода get и post
# class WomenAPIList(generics.ListCreateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#
# class WomenAPIUpdate(generics.UpdateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#
# class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

# class WomenAPIView(APIView):
#     def get(self, request):
#         # получаем значение полей
#         w = Women.objects.all()
#         # many=True говорит что передовать и получать мы будем список записей
#         return Response({'posts': WomenSerializer(w, many=True).data})
#
#     def post(self, request):
#         # создаём сериализатор на основе данных полученных из реквест запроса
#         serializer = WomenSerializer(data=request.data)
#         # с помощю is_vlaid проверяем коректность принятых данных
#         serializer.is_valid(raise_exception=True)
#         # добавление записи в бд
#         serializer.save()
#
#         # в качестве ответа возвращаем данные которые мы добавили
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error': 'Method PUT not allowed'})
#
#         try:
#             instance = Women.objects.get(pk=pk)
#         except:
#             return Response({'error': 'Object does not exists'})
#
#         # создаёа обьект сериалайзер передаём в него данные из реквеста и модель найденную по пк
#         serializer = WomenSerializer(data=request.data, instance=instance)
#         # проверяем
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # возвращаем данные сериалайзера
#         return Response({'post': serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error': 'Method PUT not allowed'})
#
#         try:
#             instance = Women.objects.get(pk=pk)
#         except:
#             return Response({'error': 'Object does not exists'})
#
#         # создаёа обьект сериалайзер передаём в него данные из реквеста и модель найденную по пк
#         serializer = WomenSerializer(instance=instance)
#
#
#         # возвращаем данные сериалайзера
#         return Response({'post': 'delete post' + serializer.data['title']})
