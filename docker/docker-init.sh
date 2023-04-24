#!/usr/bin/env bash

set -e

superset db upgrade

superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin

superset init

superset set_database_uri -d spotify_db -u postgresql+psycopg2://postgres:postgres@spotify_db:5432/postgres
