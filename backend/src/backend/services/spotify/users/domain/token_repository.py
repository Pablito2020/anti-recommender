from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.backend.common.result import Result, Error


class SpotifyToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str
    id_token: str


class Token(SpotifyToken):
    expires_at: float


class TokenRepository(ABC):
    @abstractmethod
    def get_token(self) -> Result[Token, Error]:
        raise NotImplementedError("Abstract class should implement getting token")

    @abstractmethod
    def refresh_token(self) -> Result[Token, Error]:
        raise NotImplementedError("Abstract class should implement adding token")
