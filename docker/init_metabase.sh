#!/usr/bin/env bash

export MB_SETUP_TOKEN=$(curl -s -m 5 -X GET \
    -H "Content-Type: application/json" \
    http://metabase:3000/api/session/properties \
    | jq -r '.["setup-token"]'
)

export MB_SESSION_TOKEN=$(
  curl -s -X POST \
      -H "Content-type: application/json" \
      http://metabase:3000/api/setup \
      -d '{
      "token": "'${MB_SETUP_TOKEN}'",
      "user": {
          "email": "'${MB_EMAIL}'",
          "first_name": "'${MB_FIRST_NAME}'",
          "last_name": "'${MB_LAST_NAME}'",
          "password": "'${MB_PASSWORD}'"
      },
      "prefs": {
          "allow_tracking": true,
          "site_name": "Spotify Charts Pipeline"
      }
  }' | jq -r '.["id"]'
)

curl -s -X POST \
    -H "Content-type: application/json" \
    -H "X-Metabase-Session: ${MB_SESSION_TOKEN}" \
    http://metabase:3000/api/database \
    -d '{
    "name": "Spotify DB",
    "engine": "postgres",
    "details": {
        "user": "'${POSTGRES_USER}'",
        "password": "'${POSTGRES_PASSWORD}'",
        "port": "'${POSTGRES_PORT}'",
        "host": "spotify_db",
        "dbname": "'${POSTGRES_DB}'"
    }
  }'
