#!/usr/bin/env bash

git clone https://github.com/JeffersonLab/xmsg_python.git ./claraweb/build/xmsg
git clone https://github.com/JeffersonLab/clara-python.git ./claraweb/build/clara

cd claraweb
python manage.py makemigrations DPE --settings=settings.base
python manage.py makemigrations Container --settings=settings.base
python manage.py makemigrations Service --settings=settings.base
python manage.py migrate --settings=settings.base --run-syncdb --no-input
docker-compose -f ../scripts/docker-compose.dev.yml build
docker-compose -f ../scripts/docker-compose.dev.yml up -d

