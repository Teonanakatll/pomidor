

from django.db.models import Count, When, Case, Avg, F
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BooksSerializer, UserBookRelationSerializer

# Добавление дополнительных действий в маршрутизацию
# Если у вас есть специальные методы, которые должны быть маршрутизируемыми, вы можете пометить их как таковые с помощью
# декоратора @action. Как и обычные действия, дополнительные действия могут быть предназначены как для одного объекта,
# так и для целой коллекции. Чтобы указать это, установите аргумент detail в True или False. Маршрутизатор настроит свои
# шаблоны URL соответствующим образом. Например, DefaultRouter настроит подробные действия так, чтобы они содержали pk в
# своих шаблонах URL. Два новых действия будут доступны по адресам ^users/{pk}/set_password/$ и
# ^users/{pk}/unset_password/$
class BookViewSet(ModelViewSet):
    # F-класс служот для обращения к полям текущей модели в орм запросах
    # Q-класс служит для записи условий фильтрации полей текущей модели при логических конструкциях в орм джанго
    # select_related() - выбирает один обьект связанный с книгой (ForeignKey)
    # prefetch_related() - выбирает все связанные обьекты (ManyToMany)
    queryset = Book.objects.all().annotate(annotated_likes=
                                           Count(Case(When(userbookrelation__like=True, then=1))),
                                           rating=Avg('userbookrelation__rate'),
                                           price_with_discount=(F('price')-(F('price') / 100) * F('discount')))\
                                           .select_related('owner').prefetch_related('readers').order_by('id')
    serializer_class = BooksSerializer
    # фильтрация, поиск и сортировка drf ?filter=, ?search= , ?ordering=
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # фильтрация по полям, значение в фильтр передаётся get запросом, в
    # новых версиях называется filterset_fields
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    # переопределяем метод для того чтобы добавить юзера в сериализатор
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
        # print('created', created)

        return obj
