FROM python:3.8.1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install ripgrep
RUN mkdir /code
WORKDIR /code
COPY dev-requirements.txt .
RUN pip install -r dev-requirements.txt
ADD . /code

ENV PYTHONPATH .
