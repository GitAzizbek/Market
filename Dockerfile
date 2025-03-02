FROM python:3.9-alpine3.16

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /temp/requirements.txt
COPY server /server
WORKDIR /server
EXPOSE 8000

# RUN apk add postgresql-client build-base postgresql-dev
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt


