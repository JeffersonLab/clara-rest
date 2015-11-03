#!/usr/bin/env python
#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

from __future__ import absolute_import
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClaraWebREST.settings')

SECRET_KEY = 'h&@82v87p&lg7bub@b(alnt6+i*-qk518+v_y)v_54%qm7-&6h'
DEBUG = True
TEMPLATE_DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True

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

    # Pipeline
    'pipeline',

    # Clara apps
    'Nodes',
    'Nodes.Container',
    'Nodes.Container.Service',
    'Applications',
    'RuntimeDataRegistrar',
    'ui',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',

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

ROOT_URLCONF = 'ClaraWebREST.urls'

WSGI_APPLICATION = 'ClaraWebREST.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# STATICS ###################################################################
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
STATIC_URL = '/static/'
# CHANGE FOR PRODUCTION #
STATIC_ROOT = 'ui/assets'
#########################
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)
STATIC_FILES_DIRS = (
    os.path.join(BASE_DIR, 'ui/assets/'),
)

# PIPELINE ##################################################################
BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'ui/assets')
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_CSSMIN_BINARY = '/usr/bin/env cssmin'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuiCompressor'
PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'bower_components/primer-css/css/primer.css',
            'bower_components/octicons/octicons/octicons.css',
            'css/style.css',
        ),
        'output_filename': 'libs.min.css',
    }
}
PIPELINE_JS = {
    'libraries': {
        'source_filenames': (
            'bower_components/highcharts-release/highcharts.src.js',
            'js/runtime_graphs.js',
        ),
        'output_filename': 'libs.min.js',
    }
}

# LOCAL AND INTERNATIONALIZATION ############################################
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False
