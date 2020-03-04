FROM python:3.7.6-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD python api.py
