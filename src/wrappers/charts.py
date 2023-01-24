import logging
from dataclasses import dataclass
from logging import Logger

import pandas as pd
from sqlalchemy import select

from src.clients.postgres import PostgresClient
from src.clients.spotify import SpotifyClient
from src.models.charts import Charts

log: Logger = logging.getLogger()


@dataclass
class ChartsWrapper:
    def __post_init__(self) -> None:
        self.spotify: SpotifyClient = SpotifyClient()
        self.postgres: PostgresClient = PostgresClient()

    def run(self, daily_chart: dict, chart_date: str, country_code: str) -> None:
        chart: pd.DataFrame = self._parse_chart_metadata(daily_chart)
        self._load_chart(chart, chart_date, country_code)

    @staticmethod
    def _parse_chart_metadata(daily_charts: dict) -> pd.DataFrame:
        df = pd.json_normalize(daily_charts["displayChart"]["chartMetadata"])

        df.columns = [col.split(".")[-1] for col in df.columns]
        df["latestDate"] = pd.to_datetime(df["latestDate"])
        df["earliestDate"] = pd.to_datetime(df["earliestDate"])

        return df

    def _load_chart(self, charts: pd.DataFrame, chart_date, country_code):
        for _, row in charts.iterrows():
            result = self.postgres.session.execute(select(Charts).filter_by(uri=row["uri"]))
            exists = result.scalars().first()

            if not exists:
                chart = Charts(
                    uri=row["uri"],
                    alias=row["alias"],
                    entityType=row["entityType"],
                    readableTitle=row["readableTitle"],
                    backgroundColor=row["backgroundColor"],
                    textColor=row["textColor"],
                    latestDate=row["latestDate"],
                    earliestDate=row["earliestDate"],
                    country=row["country"],
                    chartType=row["chartType"],
                    recurrence=row["recurrence"],
                )
                self.postgres.session.add(chart)
                self.postgres.session.commit()
                log.info(
                    f"[{chart_date}] [{country_code}] - Added chart to database: {row['readableTitle']} ({row['uri']})"
                )

            else:
                log.warning(
                    f"[{chart_date}] [{country_code}] - Chart already exists in database:"
                    f" {row['readableTitle']} ({row['uri']})"
                )
