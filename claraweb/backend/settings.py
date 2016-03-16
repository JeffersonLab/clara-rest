#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claraweb.backend.settings')

SECRET_KEY = 'h&@82v87p&lg7bub@b(alnt6+i*-qk518+v_y)v_54%qm7-&6h'
DEBUG = True
TEMPLATE_DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True

# Django Testing Logger
logging.disable(logging.CRITICAL)

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # REST Framework
    'rest_framework',
    'rest_framework_swagger',

    #extensions
    'django_extensions',

    # Clara apps
    'claraweb.rest.DPE',
    'claraweb.rest.Container',
    'claraweb.rest.Service',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework_yaml.parsers.YAMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_yaml.renderers.YAMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

ROOT_URLCONF = 'claraweb.backend.urls'

WSGI_APPLICATION = 'claraweb.backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# STATICS ###################################################################
STATIC_URL = '/static/'
STATIC_ROOT = '/assets'
#########################
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_FILES_DIRS = (
    os.path.join(BASE_DIR, '/assets/'),
)

# LOCAL AND INTERNATIONALIZATION ############################################
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False
