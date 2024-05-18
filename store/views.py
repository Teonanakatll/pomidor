from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from store.models import Book
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BooksSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    # фильтрация, поиск и сортировка drf ?filter=, ?search= , ?ordering=
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # фильтрация по полям, значение в фильтр передаётся get запросом, в
    # новых версиях называется filterset_fields
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    # переопределяем метод для того чтобы добавить юзера
    def perform_create(self, serializer):
        # донные сериолизатора после того как он прошёл валидацию, добавляем юзера из request
        # так как create-запрос у нас может делать только зарегистрированный пользователь проверять не надо
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

def auth(request):
    return render(request, 'store/oauth.html')