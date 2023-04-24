# Spotify Charts Pipeline

Get the daily [Spotify Charts](https://charts.spotify.com/charts/overview/global) data history and load to a PostgreSLQ database

![](https://user-images.githubusercontent.com/20917430/215230710-de0a4f85-3d98-4ad5-8367-c6739ee17347.png)

## Set up

1. Register on [Spotify Developer](https://developer.spotify.com/dashboard/)
2. Create an app
3. Add a Redirect URI to the app (e.g. `http://localhost:9000`)

## Poetry
Poetry is a python dependency management tool to manage dependencies, packages, and libraries in your python project. 
Install it by following the [official documentation](https://python-poetry.org/docs/#installation)

## Running

Clone the repository
````bash
git clone https://github.com/felipeall/spotify-charts-pipeline.git
````

Access the project root folder
````bash
cd spotify-charts-pipeline
````

Create a `.env` file and add your `CLIENT_ID`, `SECRET_ID` and `REDIRECT_URI`
```bash
cp .env.template .env
```

Create a Poetry virtual environment
````bash
poetry shell
````

Install the required packages
````bash
poetry install
````

Instantiate the PostgreSQL docker container
````bash
docker compose -p spotify_charts up -d --build
````

Run the pipeline with the desired arguments
````bash
python src/main.py [from_date] [to_date] [country_code]
````

Example
````bash
python src/main.py --from_date 2023-01-01 --to_date 2023-01-31 --country_code BR
````
## Unit tests
````bash
docker compose -f docker-compose.tests.yml up --build --abort-on-container-exit --remove-orphans ; docker compose -f docker-compose.tests.yml rm -fsv
````
