"""
URL configuration for books project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from drf.views import WomenAPIList, \
    WomenAPIUpdate, WomenAPIDestroy  # WomenViewSet, WomenAPIList, WomenAPIUpdate, WomenAPIDetailView,   # WomenAPIView,
from store.views import BookViewSet

router_book = SimpleRouter()
router_women = DefaultRouter()
# при использовании DefaultRouter можно обращаться к корню маршрутов (api/v1/) чтобы получить запись, и автоматически
# появляются имена у маршрутов по имени моделей

# регистрируем наш путь в роутере, можно использовать необязательный аргумент namespase=,
# basename=  используется если  нет параметра queryset
router_book.register(r'book', BookViewSet)
# router_women.register(r'women', WomenViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # авторизация на основе сессий и cookies
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    # path('api/v1/', include(router_book.urls)),
    # path('api/v1/', include(router_women.urls)),
    path('api/v1/women/', WomenAPIList.as_view()),
    path('api/v1/women/<int:pk>/', WomenAPIUpdate.as_view()),
    path('api/v1/womendelete/<int:pk>/', WomenAPIDestroy.as_view()),
    # path('api/v1/womenlist/', WomenAPIList.as_view()),
    # для ViewSet можно дополнительно прописывать метод и функцию которая будет его обрабатывать
    # path('api/v1/womenlist/', WomenViewSet.as_view({'get': 'list'})),
    # path('api/v1/womendetail/<int:pk>/', WomenViewSet.as_view({'put': 'update'})),
    # path('api/v1/womenlist/<int:pk>/', WomenAPIUpdate.as_view()),
    # path('api/v1/womendetail/<int:pk>/', WomenAPIDetailView.as_view()),
]