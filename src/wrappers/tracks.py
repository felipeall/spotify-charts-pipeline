import logging
from dataclasses import dataclass
from logging import Logger

import numpy as np
import pandas as pd
from sqlalchemy import select

from src.clients.postgres import PostgresClient
from src.clients.spotify import SpotifyClient
from src.models.tracks import Tracks

log: Logger = logging.getLogger()


@dataclass
class TracksWrapper:
    """Transform and load tracks' metadata"""

    def __post_init__(self) -> None:
        """Instantiate Spotify and Postgres clients"""
        self.spotify: SpotifyClient = SpotifyClient()
        self.postgres: PostgresClient = PostgresClient()

    def run(self, daily_chart: dict, chart_date: str, country_code: str) -> None:
        """Run the Tracks Wrapper, which extracts the tracks' metadata from the daily chart and uploads to the
        database the records that doesn't exist.

        :param daily_chart: Daily chart data extracted from the Spotify API
        :param chart_date: Date of the chart being processed
        :param country_code: Code of the country being processed
        """
        tracks: pd.DataFrame = self._extract_tracks_metadata(daily_chart)
        self._load_tracks(tracks, chart_date, country_code)

    @staticmethod
    def _extract_tracks_metadata(daily_charts: dict) -> pd.DataFrame:
        """Parse the daily chart data by extracting the tracks' metadata.

        :param daily_charts: Daily chart data extracted from the Spotify API
        :return: Parsed tracks' metadata
        """
        tracks = (
            pd.json_normalize(daily_charts["entries"])
            .pipe(lambda df: df.loc[:, [col for col in df.columns if col.startswith("trackMetadata.")]])
            .pipe(lambda df: df.set_axis([col.split(".")[-1] for col in df.columns], axis=1))
            .assign(artistUri=lambda x: x["artists"].apply(lambda y: [row["spotifyUri"] for row in y]))
            .assign(labels=lambda x: x["labels"].apply(lambda y: [row["name"] for row in y]))
            .drop(columns=["artists"])
            .replace(np.nan, None)
        )

        return tracks

    def _load_tracks(self, tracks: pd.DataFrame, chart_date: str, country_code: str) -> None:
        """Load to the database the tracks records that doesn't exist yet.

        :param tracks: Parsed tracks' metadata
        :param chart_date: Date of the chart being processed
        :param country_code: Code of the country being processed
        """
        for _, row in tracks.iterrows():
            result = self.postgres.session.execute(select(Tracks).filter_by(trackUri=row["trackUri"]))
            exists = result.scalars().first()

            if not exists:
                track = Tracks(
                    trackUri=row["trackUri"],
                    trackName=row["trackName"],
                    displayImageUri=row["displayImageUri"],
                    artistUri=row["artistUri"],
                    labels=row["labels"],
                    releaseDate=row["releaseDate"],
                )
                self.postgres.session.add(track)
                self.postgres.session.commit()
                log.info(
                    f"[{chart_date}] [{country_code}] - Added track to database: {row['trackName']} ({row['trackUri']})"
                )

            else:
                log.warning(
                    f"[{chart_date}] [{country_code}] - Track already exists in database:"
                    f" {row['trackName']} ({row['trackUri']})"
                )
