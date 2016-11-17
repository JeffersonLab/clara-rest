#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

SECRET_KEY = 'h&@82v87p&lg7bub@b(alnt6+i*-qk518+v_y)v_54%qm7-&6h'
CORS_ORIGIN_ALLOW_ALL = True

# Django Testing Logger
logging.disable(logging.CRITICAL)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # REST Framework
    'rest_framework',
    'rest_framework_swagger',

    # Clara apps
    'claraweb.backend.rest.DPE.apps.DPEConfig',
    'claraweb.backend.rest.Container.apps.ContainerConfig',
    'claraweb.backend.rest.Service.apps.ServiceConfig',
]

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

# STATICS ###################################################################
STATIC_URL = '/static/'
STATIC_ROOT = '/assets'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_FILES_DIRS = (
    os.path.join(BASE_DIR, '/assets/'),
)

# SWAGGER ###################################################################
SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '1.0',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': False,
    'is_superuser': False,
    'unauthenticated_user': 'django.contrib.auth.models.AnonymousUser',
    'permission_denied_handler': None,
    'resource_access_handler': None,
    'info': {
        'contact': 'oyarzun@jlab.org',
        'description': 'This is a Clara REST server. ',
        'termsOfServiceUrl': '',
        'title': 'Clara REST server',
    },
    'doc_expansion': 'none',
}

# LOCAL AND INTERNATIONALIZATION ############################################
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False
