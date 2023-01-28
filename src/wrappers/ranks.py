import logging
from dataclasses import dataclass
from logging import Logger

import pandas as pd
from sqlalchemy import select

from src.clients.postgres import PostgresClient
from src.clients.spotify import SpotifyClient
from src.models.ranks import Ranks

log: Logger = logging.getLogger()


@dataclass
class RanksWrapper:
    """Transform and load ranks' metadata"""

    def __post_init__(self) -> None:
        """Instantiate Spotify and Postgres clients"""
        self.spotify: SpotifyClient = SpotifyClient()
        self.postgres: PostgresClient = PostgresClient()

    def run(self, daily_chart: dict, chart_date: str, country_code: str) -> None:
        """Run the Ranks Wrapper, which extracts the ranks' metadata from the daily chart and uploads to the
        database the records that doesn't exist.

        :param daily_chart: Daily chart data extracted from the Spotify API
        :param chart_date: Date of the chart being processed
        :param country_code: Code of the country being processed
        """
        ranks: pd.DataFrame = self._extract_ranks_metadata(daily_chart)
        self._load_ranks(ranks, chart_date, country_code)

    @staticmethod
    def _extract_ranks_metadata(daily_charts: dict) -> pd.DataFrame:
        """Parse the daily chart data by extracting the ranks' metadata.

        :param daily_charts: Daily chart data extracted from the Spotify API
        :return: Parsed ranks' metadata
        """
        ranks: pd.DataFrame = (
            pd.json_normalize(daily_charts["entries"])
            .pipe(lambda df: df.set_axis([col.split(".")[-1] for col in df.columns], axis=1))
            .drop(columns=["displayImageUri", "artists", "labels", "releaseDate"])
            .rename(columns={"value": "metricValue", "type": "metricType"})
            .assign(chartUri=daily_charts["displayChart"]["chartMetadata"]["uri"])
            .assign(date=daily_charts["displayChart"]["date"])
        )

        return ranks

    def _load_ranks(self, ranks: pd.DataFrame, chart_date: str, country_code: str) -> None:
        """Load to the database the ranks records that doesn't exist yet.

        :param ranks: Parsed ranks' metadata
        :param chart_date: Date of the chart being processed
        :param country_code: Code of the country being processed
        """
        for _, row in ranks.iterrows():
            result = self.postgres.session.execute(
                select(Ranks).filter_by(
                    chartUri=row["chartUri"],
                    date=row["date"],
                    currentRank=row["currentRank"],
                )
            )
            exists = result.scalars().first()

            if not exists:
                rank = Ranks(
                    chartUri=row["chartUri"],
                    date=row["date"],
                    trackUri=row["trackUri"],
                    currentRank=row["currentRank"],
                    previousRank=row["previousRank"],
                    peakRank=row["peakRank"],
                    appearancesOnChart=row["appearancesOnChart"],
                    consecutiveAppearancesOnChart=row["consecutiveAppearancesOnChart"],
                    metricValue=row["metricValue"],
                    metricType=row["metricType"],
                    entryStatus=row["entryStatus"],
                    peakDate=row["peakDate"],
                    entryRank=row["entryRank"],
                    entryDate=row["entryDate"],
                )
                self.postgres.session.add(rank)
                self.postgres.session.commit()
                log.info(
                    f"[{chart_date}] [{country_code}] - Added rank position to database:"
                    f" #{row['currentRank']} ({row['chartUri']})"
                )

            else:
                log.warning(
                    f"[{chart_date}] [{country_code}] - Rank position already exists in database:"
                    f" #{row['currentRank']} ({row['chartUri']})"
                )
