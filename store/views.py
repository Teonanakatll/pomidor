from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BooksSerializer, UserBookRelationSerializer


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

class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    # lookup_field - Поле цели, которое должно быть использовано для поиска. Должно соответствовать
    # аргументу ключевого слова URL в ссылающемся представлении.
    lookup_field = 'book'

    # в lookup_field мы передаём id книги, но этого недастаточно, нужно ещё передать id юзера чтобы найти
    # эту связь, в UserBookRelation два поля ForeignKey, переопределим метод get_object
    def get_object(self):
        # если юзер первый раз ставит лайк то мы не сможем получить его UserBookRelation, в таком случае создаём эту свзь
        # передаём юзера и именованный параметр 'book' пришедший через lookup_field
        obj, created = UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])
        print('created', created)

        return obj
