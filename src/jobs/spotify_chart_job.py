import logging
from dataclasses import dataclass
from datetime import date, datetime
from logging import Logger

import pandas as pd

from src.clients.spotify import SpotifyClient
from src.wrappers.artists import ArtistsWrapper
from src.wrappers.charts import ChartsWrapper
from src.wrappers.ranks import RanksWrapper
from src.wrappers.tracks import TracksWrapper

log: Logger = logging.getLogger()


@dataclass
class SpotifyChartJob:
    from_date: str
    to_date: str
    country_code: str

    def __post_init__(self) -> None:
        self.charts_wrapper: ChartsWrapper = ChartsWrapper()
        self.tracks_wrapper: TracksWrapper = TracksWrapper()
        self.artists_wrapper: ArtistsWrapper = ArtistsWrapper()
        self.ranks_wrapper: RanksWrapper = RanksWrapper()
        self.spotify_client: SpotifyClient = SpotifyClient()

    def run(self) -> None:
        self._validate_country_code_arg()
        self._validate_date_args()

        job_parameters: list = self._construct_job_parameters()

        for chart_date in job_parameters:
            log.info(f"[{chart_date}] [{self.country_code}] - Getting daily chart...")
            daily_chart: dict = self.spotify_client.get_daily_chart(
                chart_date=chart_date, country_code=self.country_code,
            )

            if not daily_chart:
                log.error(f"[{chart_date}] [{self.country_code}] - Daily chart not available!")
                continue

            self.charts_wrapper.run(daily_chart=daily_chart, chart_date=chart_date, country_code=self.country_code)
            self.tracks_wrapper.run(daily_chart=daily_chart, chart_date=chart_date, country_code=self.country_code)
            self.artists_wrapper.run(daily_chart=daily_chart, chart_date=chart_date, country_code=self.country_code)
            self.ranks_wrapper.run(daily_chart=daily_chart, chart_date=chart_date, country_code=self.country_code)

    def _construct_job_parameters(self) -> list:
        return [str(d.date()) for d in pd.date_range(self.from_date, self.to_date)]

    def _validate_country_code_arg(self) -> None:
        country_codes: list = [
            "GLOBAL",
            "AR",
            "AU",
            "AT",
            "BY",
            "BE",
            "BO",
            "BR",
            "BG",
            "CA",
            "CL",
            "CO",
            "CR",
            "CY",
            "CZ",
            "DK",
            "DO",
            "EC",
            "EG",
            "SV",
            "EE",
            "FI",
            "FR",
            "DE",
            "GR",
            "GT",
            "HN",
            "HK",
            "HU",
            "IS",
            "IN",
            "ID",
            "IE",
            "IL",
            "IT",
            "JP",
            "KZ",
            "LV",
            "LT",
            "LU",
            "MY",
            "MX",
            "MA",
            "NL",
            "NZ",
            "NI",
            "NG",
            "NO",
            "PK",
            "PA",
            "PY",
            "PE",
            "PH",
            "PL",
            "PT",
            "RO",
            "SA",
            "SG",
            "SK",
            "ZA",
            "KR",
            "ES",
            "SE",
            "CH",
            "TW",
            "TH",
            "TR",
            "AE",
            "UA",
            "GB",
            "UY",
            "US",
            "VE",
            "VN",
        ]

        if self.country_code.upper() not in country_codes:
            log.critical(f"`{self.from_date}` is an invalid `country_code` argument")
            raise SystemExit

    def _validate_date_args(self) -> None:
        try:
            from_date_parsed = datetime.strptime(self.from_date, "%Y-%m-%d")
        except ValueError:
            log.critical(f"`{self.from_date}` is an invalid `from_date` argument format, please use `YYYY-MM-DD`")
            raise SystemExit

        try:
            to_date_parsed = datetime.strptime(self.to_date, "%Y-%m-%d")
        except ValueError:
            log.critical(f"`{self.to_date}` is an invalid `to_date` argument format, please use `YYYY-MM-DD`")
            raise SystemExit

        if from_date_parsed < datetime(2017, 1, 1):
            log.critical(f"`{self.from_date}` is an invalid `from_date` argument, should be >= `2017-01-01`")
            raise SystemExit

        if to_date_parsed > datetime.today():
            log.critical(
                f"`{self.to_date}` is an invalid `to_date` argument, should be <= `{date.today().isoformat()}`",
            )
            raise SystemExit

        if from_date_parsed >= to_date_parsed:
            log.critical(
                f"`from_date {self.from_date}` and `to_date {self.to_date}` are invalid arguments, Please use"
                " `from_date` < `to_date`",
            )
            raise SystemExit
