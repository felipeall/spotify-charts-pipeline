ARG FROM_CONTAINER_NAME=public.ecr.aws/docker/library/python
FROM --platform=linux/amd64 ${FROM_CONTAINER_NAME}:${PYTHON_RELEASE:-3.9.16}-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y curl jq

RUN mkdir -p /app

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN pip3 install --upgrade pip \
    && pip3 install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

COPY . /app
ENV PYTHONPATH /app
