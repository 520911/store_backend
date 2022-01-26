FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /shop
COPY . /shop
WORKDIR /shop