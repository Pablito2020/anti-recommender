import time
from dataclasses import dataclass

import requests

from backend.common.result import Result, Error
from backend.services.spotify.users.domain import TokenRepository, Token

OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"


@dataclass
class SpotifyToken(TokenRepository):  # type: ignore
    """
    Reverse-engineered requests for refreshing a spotify token
    You should specify the user_id, where
    """

    user_id: str
    token: Token

    def get_token(self) -> Result[Token, Error]:
        return Result(success=self.token)

    def refresh_token(self) -> Result[Token, Error]:
        # TODO: Check for a lot of errors here!
        payload = {
            "refresh_token": self.token.refresh_token,
            "grant_type": "refresh_token",
            "client_id": self.user_id,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(OAUTH_TOKEN_URL, data=payload, headers=headers)
        response.raise_for_status()
        token_info = response.json()
        token_info["expires_at"] = int(time.time()) + token_info["expires_in"]
        new_token = Token(**token_info)
        self.token = new_token
        return Result(success=new_token)
