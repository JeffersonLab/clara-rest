# coding=utf-8

from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'restdb',
        'HOST': 'db',
        'USER': 'rest',
        'PASSWORD': '123',
    }
}
