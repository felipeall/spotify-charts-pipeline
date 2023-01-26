ARG FROM_CONTAINER_NAME=public.ecr.aws/docker/library/python
FROM --platform=linux/amd64 ${FROM_CONTAINER_NAME}:${PYTHON_RELEASE:-3.9.16}-slim-buster

RUN apt-get update -y && apt-get upgrade -y && apt-get install build-essential libpq-dev -y

RUN mkdir -p /opt/app

WORKDIR /opt/app
COPY poetry.lock pyproject.toml ./

RUN pip3 install --upgrade pip \
    && pip3 install poetry \
    && poetry config virtualenvs.create false \
    && poetry install
