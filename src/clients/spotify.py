import logging
import os
from dataclasses import dataclass
from json import JSONDecodeError
from logging import Logger
from typing import Optional

import requests
from dotenv import load_dotenv
from requests import Response
from spotipy import SpotifyOAuth

log: Logger = logging.getLogger()
load_dotenv()


@dataclass
class SpotifyClient:
    CLIENT_ID: str = os.environ.get("CLIENT_ID")
    CLIENT_SECRET: str = os.environ.get("CLIENT_SECRET")
    REDIRECT_URI: str = os.environ.get("REDIRECT_URI")

    def __post_init__(self) -> None:
        spotify_auth: SpotifyOAuth = SpotifyOAuth(
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            redirect_uri=self.REDIRECT_URI,
        )
        self.token: str = spotify_auth.get_access_token(as_dict=False)

    def get_daily_chart(self, country_code: str, chart_date: str) -> Optional[dict]:
        url: str = (
            f"https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-{country_code}-daily/{chart_date}"
        )
        response: Response = self._get(url)
        try:
            return response.json()
        except JSONDecodeError:
            return None

    def _get(self, url: str) -> Response:
        headers: dict = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        return requests.get(url, headers=headers)
