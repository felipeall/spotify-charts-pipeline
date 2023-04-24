FROM apache/superset:2.0.1

# Switching to root to install the required packages
USER root
COPY --chown=superset:superset ./superset/assets .
RUN pip install psycopg2-binary
USER superset
RUN superset fab create-admin \
              --username superset \
              --firstname Superset \
              --lastname Admin \
              --email admin@example.com \
              --password superset
RUN superset db upgrade
RUN superset init
#RUN superset set_database_uri -d OLTP  -u postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@oltp:5432/sales_oltp
#RUN superset set_database_uri -d DW  -u postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@dw:5432/sales_dw
RUN superset set_database_uri -d spotify_db -u postgresql+psycopg2://postgres:postgres@spotify_db:5432/postgres
#RUN superset import-dashboards -p ./dashboard.json