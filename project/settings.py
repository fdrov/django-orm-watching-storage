import os
from decouple import config, Csv
from dj_database_url import parse as db_url

DATABASES = {
    'default': config('DATABASE_URL', cast=db_url)
}

INSTALLED_APPS = ['datacenter']

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool)

ROOT_URLCONF = "project.urls"

ALLOWED_HOSTS = config('ALLOW_HOSTS', default='127.0.0.1', cast=Csv())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
    },
]


USE_L10N = True

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_TZ = True
