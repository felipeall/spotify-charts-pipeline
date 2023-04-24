import argparse
from datetime import date, timedelta

from loguru import logger as log

from src.jobs.spotify_chart_job import SpotifyChartJob

if __name__ == "__main__":
    log.info("Starting Spotify Charts Pipeline...")

    # Argument parser
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--from_date", type=str, default=(date.today() - timedelta(days=2)).isoformat())
    parser.add_argument("--to_date", type=str, default=(date.today() - timedelta(days=1)).isoformat())
    parser.add_argument("--country_code", type=str, default="GLOBAL")
    args: argparse.Namespace = parser.parse_args()

    # Set up
    FROM_DATE: str = args.from_date
    TO_DATE: str = args.to_date
    COUNTRY_CODE: str = args.country_code

    # Logging
    log.info(f"{COUNTRY_CODE=}")
    log.info(f"{FROM_DATE=}")
    log.info(f"{TO_DATE=}")

    # Job
    job: SpotifyChartJob = SpotifyChartJob(from_date=FROM_DATE, to_date=TO_DATE, country_code=COUNTRY_CODE)

    # Run
    job.run()

    log.info("Finished Spotify Charts Pipeline!")
