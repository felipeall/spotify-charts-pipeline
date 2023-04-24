from dataclasses import dataclass

import pandas as pd
from loguru import logger as log
from sqlalchemy import select

from src.clients.postgres import PostgresClient
from src.clients.spotify import SpotifyClient
from src.models.charts import Charts


@dataclass
class ChartsWrapper:
    """Transform and load charts' metadata"""

    def __post_init__(self) -> None:
        """Instantiate Spotify and Postgres clients"""
        self.spotify: SpotifyClient = SpotifyClient()
        self.postgres: PostgresClient = PostgresClient()

    def run(self, daily_chart: dict, chart_date: str, country_code: str) -> None:
        """Run the Charts Wrapper, which extracts the charts' metadata from the daily chart and uploads to the
        database the records that doesn't exist.

        :param daily_chart: Daily chart data extracted from the Spotify API
        :param chart_date: Date of the chart being processed
        :param country_code: Code of the country being processed
        """
        charts: pd.DataFrame = self._extract_charts_metadata(daily_chart)
        self._load_charts(charts, chart_date, country_code)

    @staticmethod
    def _extract_charts_metadata(daily_charts: dict) -> pd.DataFrame:
        """Parse the daily chart data by extracting the charts' metadata.

        :param daily_charts: Daily chart data extracted from the Spotify API
        :return: Parsed charts' metadata
        """
        charts: pd.DataFrame = (
            pd.json_normalize(daily_charts["displayChart"]["chartMetadata"])
            .pipe(lambda df: df.set_axis([col.split(".")[-1] for col in df.columns], axis=1))
            .assign(latestDate=lambda x: pd.to_datetime(x["latestDate"]))
            .assign(earliestDate=lambda x: pd.to_datetime(x["earliestDate"]))
        )

        return charts

    def _load_charts(self, charts: pd.DataFrame, chart_date, country_code):
        """Load to the database the tracks records that doesn't exist yet.

        :param charts: Parsed charts' metadata
        :param chart_date: Date of the chart being processed
        :param country_code: Code of the country being processed
        """
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
                    f"[{chart_date}] [{country_code}] - Added chart to database: {row['readableTitle']} ({row['uri']})",
                )

            else:
                log.warning(
                    f"[{chart_date}] [{country_code}] - Chart already exists in database:"
                    f" {row['readableTitle']} ({row['uri']})",
                )
