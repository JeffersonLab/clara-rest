# coding=utf-8

from base import *

DEBUG = False
TEMPLATE_DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'database': 'clara-rest',
        'user': 'USER',
        'password': 'thepassword',
        'default-character-set': 'utf8',
    }
}
