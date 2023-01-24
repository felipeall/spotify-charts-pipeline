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
    def __post_init__(self) -> None:
        self.spotify: SpotifyClient = SpotifyClient()
        self.postgres: PostgresClient = PostgresClient()

    def run(self, daily_chart: dict, chart_date: str, country_code: str) -> None:
        artist: pd.DataFrame = self._parse_artist_metadata(daily_chart)
        self._load_artist(artist, chart_date, country_code)

    @staticmethod
    def _parse_artist_metadata(daily_charts: dict) -> pd.DataFrame:
        df: pd.DataFrame = pd.json_normalize(daily_charts["entries"])

        df = df.explode("trackMetadata.artists")
        df[["name", "uri"]] = df["trackMetadata.artists"].apply(pd.Series)
        df = df.loc[:, ["name", "uri"]]
        df.drop_duplicates(inplace=True)

        return df

    def _load_artist(self, artist: pd.DataFrame, chart_date: str, country_code: str) -> None:
        for _, row in artist.iterrows():
            result = self.postgres.session.execute(select(Artists).filter_by(uri=row["uri"]))
            exists = result.scalars().first()

            if not exists:
                artist = Artists(
                    uri=row["uri"],
                    name=row["name"],
                )
                self.postgres.session.add(artist)
                self.postgres.session.commit()
                log.info(f"[{chart_date}] [{country_code}] - Added artist to database: {row['name']} ({row['uri']})")

            else:
                log.warning(
                    f"[{chart_date}] [{country_code}] - Artist already exists in database: {row['name']} ({row['uri']})"
                )
