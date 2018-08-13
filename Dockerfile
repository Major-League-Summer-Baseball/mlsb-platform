FROM python:3.6

Label maintainer "Dallas Fraser <dallas.fraser.waterloo@gmail.com>"

RUN apt-get update && apt-get install -y \
        libmemcached11 \
        libmemcachedutil2 \
        libmemcached-dev \
        libz-dev

RUN mkdir /mlsb

WORKDIR /mlsb

COPY . /mlsb

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV="docker"

EXPOSE 8080