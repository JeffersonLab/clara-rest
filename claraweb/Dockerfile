FROM ubuntu:16.04

ARG DJANGO_ENV

# Prepare dependencies
RUN apt-get update
RUN apt-get -y install python-dev \
python-pip \
python-virtualenv \
libpq-dev

RUN pip install --upgrade pip

RUN mkdir -p /root/
RUN touch /root/.bashrc
RUN mkdir /root/.virtualenvs

ENV WEBAPP_DIR=/claraweb
RUN mkdir $WEBAPP_DIR
ADD . $WEBAPP_DIR/
WORKDIR $WEBAPP_DIR

ENV PYTHONUNBUFFERED=1
ADD requirements/base.txt $WEBAPP_DIR/
ADD requirements/$DJANGO_ENV.txt $WEBAPP_DIR/
WORKDIR $WEBAPP_DIR/build/xmsg/
RUN python setup.py install
WORKDIR $WEBAPP_DIR/build/clara/
RUN python setup.py install
WORKDIR $WEBAPP_DIR
RUN pip install -r $DJANGO_ENV.txt
RUN python manage.py collectstatic --settings=settings.base --no-input
