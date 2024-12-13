from dataclasses import dataclass, field
from typing import List

from backend.services.spotify.users.infra.spotify.token import (
    SpotifyToken as SpotifyTokenService,
)
from backend.services.spotify.users.infra.spotify.user import SpotifyUser

from backend.common.result import Result, Error
from backend.services.spotify.users.domain import (
    TokenRepository,
    Token,
    UserRepository,
    User,
    Mail,
)
from backend.services.spotify.users.infra.sqlite.token import SqliteTokenRepository
from backend.services.spotify.users.infra.sqlite.users import SqliteUsersRepository


@dataclass
class RepositoryImplementation(TokenRepository, UserRepository):  # type: ignore
    """
    It's a cache for our users, and a database for our tokens.
    """

    app_id: str
    user_id: str
    initial_token: str | None
    sqlite_path: str
    spotify_token: SpotifyTokenService = field(init=False)
    spotify_user: SpotifyUser = field(init=False)
    sqlite_token: SqliteTokenRepository = field(init=False)
    sqlite_user: SqliteUsersRepository = field(init=False)

    def __post_init__(self) -> None:
        self.sqlite_token = SqliteTokenRepository(
            sqlite_path=self.sqlite_path, initial_token=self.initial_token
        )
        self.sqlite_user = SqliteUsersRepository(sqlite_path=self.sqlite_path)
        initial_token = self.sqlite_token.get_token()
        if initial_token.is_error:
            raise ValueError(
                "We can't initialize infrastructure because we couldn't get initial token"
            )
        self.spotify_token = SpotifyTokenService(
            user_id=self.user_id, token=initial_token.success_value
        )
        self.spotify_user = SpotifyUser(app_id=self.app_id)

    def delete_user(self, mail: Mail, token: Token) -> Result[User, Error]:
        result = self.spotify_user.delete_user(mail, token)
        if result.is_error:
            return result
        return self.sqlite_user.delete_user(result.success_value)

    def add_user(self, mail: Mail, token: Token) -> Result[User, Error]:
        result = self.spotify_user.add_user(mail, token)
        if result.is_error:
            return result
        return self.sqlite_user.add_user(result.success_value)

    def users(self) -> Result[List[User], Error]:
        return self.sqlite_user.users()

    def refresh_token(self) -> Result[Token, Error]:
        refreshed_token_result = self.spotify_token.refresh_token()
        if refreshed_token_result.is_error:
            return refreshed_token_result
        return self.sqlite_token.add_token(refreshed_token_result.success_value)

    def get_token(self) -> Result[Token, Error]:
        return self.sqlite_token.get_token()
