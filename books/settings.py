"""
Django settings for books project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@1yq3t9qg4$_g!51$z4_gc3nagwrge%!%ysqzn^n8t4syl0350'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # чтобы debug-toolbar работол с api pip install django-debug-toolbar-force
    # чтобы видеть панель дебакера вконце каждого урла писать - ?debug-toolbar
    'debug_toolbar',

    'store.apps.StoreConfig',
    'drf.apps.DrfConfig',

    'rest_framework',
    # чтобы дрф использовал свою стандартную таблицу токенов
    'rest_framework.authtoken',
    # jwt токены
    'djoser',
    # social-auth-app-django
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware',
]

ROOT_URLCONF = 'books.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'books.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "books_db",
        "USER": "home",
        "PASSWORD": "home",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# авторизация через социальные сети, чтобы этот пакет мог пользоваться djsonfield-ом в постгресе
SOCIAL_AUTH_POSTGRES_JSONFIELD_ENABLED = True

# изменить namespace django-social
SOCIAL_AUTH_URL_NAMESPACE = 'socialll'

# <a href="{% url "social:begin" "google-oauth2" %}">Google+</a>

SOCIAL_AUTH_GITHUB_KEY = 'Ov23likMDGjlasZIuAC0'
SOCIAL_AUTH_GITHUB_SECRET = '8ead03fffc8d921a873ebc7fec56b3d138f77c57'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.twitter.TwitterOAuth',

    'social_core.backends.github.GithubOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_DIRS = []

INTERNAL_IPS = [
    '127.0.0.1',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# для управления глобальными настройками drf
REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 2,

    # отрисовка данных ответа, Сериализованные данные для дальнейшей передачи по сети нужно перевести (отрендерить) в
    # json-формат — универсальный текстовый формат передачи данных, не зависящий от языка реализации
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # api браузера (красивая отрисовка
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': (
        # Анализирует содержимое запроса JSON . request.data будет заполнен словарем данных.
        'rest_framework.parsers.JSONParser',
    )
    # глобальное ограничение доступа на уровне всего проекта
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    #     # 'rest_framework.authentication.TokenAuthentication',
    #     # 2 строчки разрешают аутентификацию по сессиям
    #     'rest_framework.authentication.BasicAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    # ]
}

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
#     "ROTATE_REFRESH_TOKENS": False,
#     "BLACKLIST_AFTER_ROTATION": False,
#     "UPDATE_LAST_LOGIN": False,
#
#     "ALGORITHM": "HS256",
#     "SIGNING_KEY": SECRET_KEY,
#     "VERIFYING_KEY": "",
#     "AUDIENCE": None,
#     "ISSUER": None,
#     "JSON_ENCODER": None,
#     "JWK_URL": None,
#     "LEEWAY": 0,
#
#     "AUTH_HEADER_TYPES": ("Bearer",),
#     "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
#     "USER_ID_FIELD": "id",
#     # внутри токена user_id будет соответствовать id пользователя
#     "USER_ID_CLAIM": "user_id",
#     "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
#
#     "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
#     "TOKEN_TYPE_CLAIM": "token_type",
#     "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
#
#     "JTI_CLAIM": "jti",
#
#     "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
#     "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
#     "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
#
#     "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
#     "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
#     "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
#     "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
#     "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
#     "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
# }
