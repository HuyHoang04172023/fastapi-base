FROM python:3.13.5

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app/requirements.txt /app/requirements.txt

RUN apt-get update -y
RUN pip install -r /app/requirements.txt
