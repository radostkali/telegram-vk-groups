FROM python:3.8.6-slim-buster

WORKDIR /usr/src/app

RUN apt-get update && apt-get install python3-dev libpq-dev -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system --dev --ignore-pipfile

COPY . .
