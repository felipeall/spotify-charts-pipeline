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
    def __post_init__(self) -> None:
        self.spotify: SpotifyClient = SpotifyClient()
        self.postgres: PostgresClient = PostgresClient()

    def run(self, daily_chart: dict, chart_date: str, country_code: str) -> None:
        rank: pd.DataFrame = self._parse_rank_metadata(daily_chart)
        self._load_rank(rank, chart_date, country_code)

    @staticmethod
    def _parse_rank_metadata(daily_charts: dict) -> pd.DataFrame:
        df: pd.DataFrame = pd.json_normalize(daily_charts["entries"])
        cols = [col for col in df.columns if col.startswith("chartEntryData.")] + ["trackMetadata.trackUri"]
        df = df.loc[:, cols]
        df.columns = [col.split(".")[-1] for col in df.columns]
        df.rename(columns={"value": "metricValue", "type": "metricType"}, inplace=True)

        df["chartUri"] = daily_charts["displayChart"]["chartMetadata"]["uri"]
        df["date"] = daily_charts["displayChart"]["date"]

        return df

    def _load_rank(self, rank: pd.DataFrame, chart_date: str, country_code: str) -> None:
        for _, row in rank.iterrows():
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
