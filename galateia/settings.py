"""
Django settings for galateia project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from sites.tass_utils import tass_circle

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p=sja%j9-v#6w#h7&9ob=f@13e+vd#8yi)zj*dj=1ro5$ut&mm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['testserver', '*']


# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_framework_swagger',
    'drf_yasg',
    'django_filters',
    'debug_toolbar',

    # user's apps
    'sites',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'galateia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

            ]
        },
    },
]

WSGI_APPLICATION = 'galateia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'galateia',
        'USER': 'galateia',
        'PASSWORD': 'Qwerty123',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Multiprocessing
PROCESS_AMOUNT = 2

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detail': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detail'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '{}/log/develop.log'.format(BASE_DIR),
            'formatter': 'detail'
        },
    },
    'loggers': {
        'tmp_develop': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

AUTH_USER_MODEL = 'users.User'

# CELERY SETTINGS
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = TIME_ZONE
CELERYD_TASK_TIME_LIMIT = 300

JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

JET_SIDE_MENU_ITEMS = [
    {'label': 'Пользователи', 'items': [
        {'name': 'users.user', 'label': 'Пользователи'},
        {'name': 'auth.group', 'label': 'Пользовательские группы'},
    ]},
    {'label': 'Сайты', 'items': [
        {'name': 'sites.site'},
        {'name': 'sites.article'},
        {'name': 'sites.usersite'},
    ]},
    {'label': 'Периодические задачи', 'items': [
        {'name': 'django_celery_beat.periodictask', 'label': 'Запланированые задачи'},
        {'name': 'django_celery_results.taskresult', 'label': 'Результат выполнения'},
        {'name': 'django_celery_beat.intervalschedule', 'label': 'Временные интервалы'}
    ]},
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
       'INTERCEPT_REDIRECTS': False,
}

INTERNAL_IPS = ('127.0.0.1', )

#todo перенести в settings_prod
#CACHES = {
#    "default": {
#        "BACKEND": "django_redis.cache.RedisCache",
#        "LOCATION": "redis://127.0.0.1:6379/1",
#        "OPTIONS": {
#            "CLIENT_CLASS": "django_redis.client.DefaultClient"
#        },
#        "KEY_PREFIX": "gpr",
#    }
#}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# конфигурирование парсеров по отдельным сайтам
#todo: вынести в отдельный модуль настроек
AVAILABLE_RENDERS = {
        'tass.ru': tass_circle,
}

STOP_WORDS = ('из', 'ничто', 'мы', 'вы', 'где', 'я', 'этот', 'тасс', 'после', 'себя', 'самый', 'вроде', 'вдоль', 'мой',
              'сквозь', 'сколько', 'некто', 'некого', 'через', 'сам', 'оно', 'они', 'над', 'она', 'когда', 'ради',
              'твой', 'всякий', 'у', 'при', 'кто', 'каждый', 'что', 'что-нибудь', 'ты', 'несколько', 'такой', 'любой',
              'в', 'по', 'навстречу', 'от', 'со', 'под', 'ничей', 'другой', 'тот', 'он', 'незачем', 'их', 'зачем', 'к',
              'кто-то', 'каковой', 'ваш', 'вследствие', 'никто', 'перед', 'какой-либо', 'столько', 'откуда', 'сей',
              'нечто', 'на', 'благодаря', 'чей', 'каков', 'иной', 'весь', 'вопреки', 'нечего', 'какой', 'до', 'с', 'её',
              'некоторый', 'о', 'без', 'близ', 'согласно', 'кроме', 'около', 'его', 'таков', 'про', 'никакой',
              'который', 'свой', 'наш', '', 'также', 'это', 'и', 'еще', 'как', 'том', 'так', 'для', 'этого', 'этом',
              'за', 'этом', 'уже', 'чтобы', 'не', 'только', 'бы', 'которых', 'а', 'изза', '-')
