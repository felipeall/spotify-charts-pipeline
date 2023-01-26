FROM public.ecr.aws/docker/library/python:3.9.15-slim
# Set up
RUN apt-get update -y && apt-get upgrade -y && apt-get install build-essential libpq-dev -y

RUN mkdir -p /opt/app

WORKDIR /opt/app
COPY poetry.lock pyproject.toml ./

RUN pip3 install --upgrade pip \
    && pip3 install poetry \
    && poetry config virtualenvs.create false \
    && poetry install
