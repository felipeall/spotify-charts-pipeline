import logging
from dataclasses import dataclass
from logging import Logger

import pandas as pd
from sqlalchemy import select

from src.clients.postgres import PostgresClient
from src.clients.spotify import SpotifyClient
from src.models.artists import Artists

log: Logger = logging.getLogger()


@dataclass
class ArtistsWrapper:
    """Transform and load artists' metadata"""

    def __post_init__(self) -> None:
        """Instantiate Spotify and Postgres clients"""
        self.spotify: SpotifyClient = SpotifyClient()
        self.postgres: PostgresClient = PostgresClient()

    def run(self, daily_chart: dict, chart_date: str, country_code: str) -> None:
        """Run the Artists Wrapper, which extracts the artists' metadata from the daily chart and uploads to the
        database the records that doesn't exist.

        :param daily_chart: Daily chart data extracted from the Spotify API
        :param chart_date: Date of the chart being processed
        :param country_code: Code of the country being processed
        """
        artists: pd.DataFrame = self._extract_artists_metadata(daily_chart)
        self._load_artists(artists, chart_date, country_code)

    @staticmethod
    def _extract_artists_metadata(daily_charts: dict) -> pd.DataFrame:
        """Parse the daily chart data by extracting the artists' metadata.

        :param daily_charts: Daily chart data extracted from the Spotify API
        :return: Parsed artists' metadata
        """
        artists: pd.DataFrame = (
            pd.json_normalize(daily_charts["entries"])
            .explode("trackMetadata.artists")
            .loc[:, "trackMetadata.artists"]
            .apply(pd.Series)
            .rename(columns={"spotifyUri": "uri"})
            .drop_duplicates()
        )

        return artists

    def _load_artists(self, artists: pd.DataFrame, chart_date: str, country_code: str) -> None:
        """Load to the database the artists records that doesn't exist yet.

        :param artists: Parsed artists' metadata
        :param chart_date: Date of the chart being processed
        :param country_code: Code of the country being processed
        """
        for _, row in artists.iterrows():
            result = self.postgres.session.execute(select(Artists).filter_by(uri=row["uri"]))
            exists = result.scalars().first()

            if not exists:
                artist: Artists = Artists(
                    uri=row["uri"],
                    name=row["name"],
                )
                self.postgres.session.add(artist)
                self.postgres.session.commit()
                log.info(f"[{chart_date}] [{country_code}] - Added artist to database: {row['name']} ({row['uri']})")

            else:
                log.warning(
                    f"[{chart_date}] [{country_code}] - "
                    f"Artist already exists in database: {row['name']} ({row['uri']})",
                )
