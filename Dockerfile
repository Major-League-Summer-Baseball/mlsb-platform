FROM python:3.7

Label maintainer "Dallas Fraser <dallas.fraser.waterloo@gmail.com>"
ENV MLSB /mlsb-platform

RUN apt-get update && apt-get install -y \
        libmemcached11 \
        libmemcachedutil2 \
        libmemcached-dev \
        libz-dev\
        unzip

RUN mkdir $MLSB

WORKDIR $MLSB

ENV PYTHONPATH="$MLSB:${PYTHONPATH}:"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_ENV="docker"

EXPOSE 8080
