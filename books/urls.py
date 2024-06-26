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
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from books import settings
from drf.views import WomenAPIList, \
    WomenAPIUpdate, WomenAPIDestroy  # WomenViewSet, WomenAPIList, WomenAPIUpdate, WomenAPIDetailView,   # WomenAPIView,
from store.views import BookViewSet, auth, UserBookRelationView

router_book = SimpleRouter()
# router_women = DefaultRouter()
# при использовании DefaultRouter можно обращаться к корню маршрутов (api/v1/) чтобы получить запись, и автоматически
# появляются имена у маршрутов по имени моделей

# регистрируем наш путь в роутере, можно использовать необязательный аргумент namespase=,
# basename=  используется если  нет параметра queryset
router_book.register(r'book', BookViewSet)
# регистрируем путь к UserBookRelation
router_book.register(r'book_relation', UserBookRelationView)
# router_women.register(r'women', WomenViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # social-django
    re_path('', include('social_django.urls', namespace='socialll')),
    path('auth/', auth),
    # path("__debug__/", include("debug_toolbar.urls")),


    # авторизация на основе сессий и cookies
    # path('api/v1/drf-auth/', include('rest_framework.urls')),

    # пути JWT
    # path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # пути djoser
    # path('api/v1/auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),


    path('', include(router_book.urls)),
    # path('api/v1/', include(router_women.urls)),
    # path('api/v1/women/', WomenAPIList.as_view()),
    # path('api/v1/women/<int:pk>/', WomenAPIUpdate.as_view()),
    # path('api/v1/womendelete/<int:pk>/', WomenAPIDestroy.as_view()),
    # path('api/v1/womenlist/', WomenAPIList.as_view()),
    # для ViewSet можно дополнительно прописывать метод и функцию которая будет его обрабатывать
    # path('api/v1/womenlist/', WomenViewSet.as_view({'get': 'list'})),
    # path('api/v1/womendetail/<int:pk>/', WomenViewSet.as_view({'put': 'update'})),
    # path('api/v1/womenlist/<int:pk>/', WomenAPIUpdate.as_view()),
    # path('api/v1/womendetail/<int:pk>/', WomenAPIDetailView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns