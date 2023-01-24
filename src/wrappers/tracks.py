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
    def __post_init__(self) -> None:
        self.spotify: SpotifyClient = SpotifyClient()
        self.postgres: PostgresClient = PostgresClient()

    def run(self, daily_chart: dict, chart_date: str, country_code: str) -> None:
        track: pd.DataFrame = self._parse_track_metadata(daily_chart)
        self._load_track(track, chart_date, country_code)

    @staticmethod
    def _parse_track_metadata(daily_charts: dict) -> pd.DataFrame:
        df: pd.DataFrame = pd.json_normalize(daily_charts["entries"])
        df = df.loc[:, df.columns.str.startswith("trackMetadata.")]
        df.columns = [col.split(".")[-1] for col in df.columns]

        df["artistUri"] = df["artists"].apply(lambda x: [row["spotifyUri"] for row in x])
        df["labels"] = df["labels"].apply(lambda x: [row["name"] for row in x])

        df = df.replace(np.nan, None)

        df.drop(columns=["artists"], inplace=True)

        return df

    def _load_track(self, track: pd.DataFrame, chart_date: str, country_code: str) -> None:
        for _, row in track.iterrows():
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
