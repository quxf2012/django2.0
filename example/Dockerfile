FROM python:3.7.0-alpine
MAINTAINER quxf2012 <quxf2012@gmail.com>
WORKDIR /code/
ADD requirements.txt requirements_dev.txt /code/
ADD requirements_dev.txt /code/
#RUN sed -i 's#http://dl-cdn.alpinelinux.org#https://mirrors.aliyun.com#' /etc/apk/repositories
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
            mysql-dev \
            g++ \
            gcc \
            libffi-dev \
    && pip install --no-cache-dir --upgrade pip \
    \
    && pip install --no-cache-dir -r requirements_dev.txt \
    && apk del .build-deps \
    \
    && find /usr/local -depth \
        \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
        -exec rm -rf '{}' + \



#&& find /usr/local -depth \
#		\( \
#			\( -type d -a \( -name test -o -name tests \) \) \
#			-o \
#			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
#		\) -exec rm -rf '{}' + \
