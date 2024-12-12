import time
from typing import List, Dict

import requests
from pydantic import BaseModel

from backend.common.result import Result, Error
from backend.services.spotify.users.domain import Token, UserRepository, Mail, User


class SpotifyUser(BaseModel, UserRepository):  # type: ignore
    app_id: str

    def users(self) -> Result[List[User], Error]:
        return Result.failure(Error("TODO: Implement get users"))

    def delete_user(self, mail: Mail, token: Token) -> Result[User, Error]:
        return Result.failure(Error("TODO: Implement delete users"))

    def add_user(self, mail: Mail, token: Token) -> Result[User, Error]:
        try:
            data = {
                "clientId": self.app_id,
                "email": mail.address,
                "name": mail.address,
            }
            response = requests.post(
                self.endpoint, json=data, headers=self._headers_from_token(token)
            )
            if response.status_code == 200:
                return Result.success(User(mail=mail, creation_date=time.time()))
            return Result.failure(
                Error(
                    f"Couldn't add user to the whitelist of the app with id: {self.app_id}. Status Code: {response.status_code}. Content: {response.content.decode()}"
                )
            )
        except Exception as e:
            return Result.failure(
                Error(f"We couldn't add user via spotify api reverse hack: {e}")
            )

    @property
    def endpoint(self) -> str:
        return (
            f"https://developer.spotify.com/api/ws4d/warp/clients/{self.app_id}/users"
        )

    def _headers_from_token(self, token: Token) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {token.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://developer.spotify.com",
            "Referer": f"https://developer.spotify.com/dashboard/{self.app_id}/users",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
        }
