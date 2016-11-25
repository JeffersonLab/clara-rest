# coding=utf-8

from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

FIXTURE_DIRS = (os.path.join(BASE_DIR, 'backend/tests/fixtures/'),)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'restdb',
        'HOST': 'db',
        'PORT': '3306'
    }
}
