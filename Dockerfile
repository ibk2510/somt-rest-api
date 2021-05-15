FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /djangoProject

WORKDIR /djangoProject

COPY requirements.txt /djangoProject/

RUN pip install -r requirements.txt

COPY . /djangoProject