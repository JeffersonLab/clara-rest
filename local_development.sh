#!/usr/bin/env bash

python claraweb/manage.py makemigrations DPE --settings=settings.base
python claraweb/manage.py makemigrations Container --settings=settings.base
python claraweb/manage.py makemigrations Service --settings=settings.base
python claraweb/manage.py migrate --settings=settings.base --run-syncdb --no-input
python claraweb/manage.py runserver --settings=settings.dev
