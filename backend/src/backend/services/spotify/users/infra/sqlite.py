import json
import os
import sqlite3
from dataclasses import dataclass, field
from json import JSONDecodeError
from typing import List

from pydantic import ValidationError

from backend.common.result import Result, Error
from backend.services.spotify.users.domain import (
    TokenRepository,
    Token,
    SpotifyToken,
    UserRepository,
    User,
    Mail,
)
from backend.services.spotify.users.infra.spotify_token import (
    SpotifyToken as SpotifyTokenService,
)
from backend.services.spotify.users.infra.spotify_user import SpotifyUser

SQLITE_PATH_ENV = "SQLITE_PATH"
INITIAL_TOKEN_ENV = "INITIAL_TOKEN"


@dataclass
class SqliteSpotifyRepository(TokenRepository, UserRepository):  # type: ignore
    """
    It's a cache for our users, and a database for our tokens.
    """

    app_id: str
    user_id: str
    sqlite_path: str | None = None
    connection: sqlite3.Connection = field(init=False)
    spotify_token: SpotifyTokenService = field(init=False)
    spotify_user: SpotifyUser = field(init=False)

    def __post_init__(self) -> None:
        self._ensure_sqlite_connection()
        self._ensure_user_table()
        self.spotify_token = SpotifyTokenService(
            user_id=self.user_id, token=self._ensure_token()
        )
        self.spotify_user = SpotifyUser(app_id=self.app_id)

    def _ensure_sqlite_connection(self) -> None:
        if self.sqlite_path is None:
            self.sqlite_path = os.environ.get(SQLITE_PATH_ENV)
        if self.sqlite_path is None:
            raise ValueError(
                f"SQLite path can't be null! Please set the env variable: {SQLITE_PATH_ENV}"
            )
        self.connection = sqlite3.connect(self.sqlite_path)

    def _ensure_user_table(self) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    mail TEXT PRIMARY KEY,
                    creation_date REAL NOT NULL
                )
                """)
            self.connection.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Users Database initialization error: {e}")

    def _ensure_token(self) -> Token:
        self._ensure_token_database()
        token_from_db = self._get_token_from_db()
        if not token_from_db:
            initial_token = self._get_initial_token_from_env_vars()
            result_saving = self._add_token_to_db(initial_token)
            if result_saving.is_error:
                raise ValueError("Error saving initial token to sqlite database")
            return result_saving.success
        if token_from_db.is_error:
            raise ValueError(
                f"Couldn't initialize sqlite repository because initial token fetching says: {token_from_db.error}"
            )
        return token_from_db.success

    def _ensure_token_database(self) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tokens (
                    access_token TEXT PRIMARY KEY,
                    token_type TEXT NOT NULL,
                    expires_in INTEGER NOT NULL,
                    refresh_token TEXT NOT NULL,
                    scope TEXT NOT NULL,
                    id_token TEXT NOT NULL,
                    expires_at REAL NOT NULL
                )
                """
            )
            self.connection.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Token Database initialization error: {e}")

    @staticmethod
    def _get_initial_token_from_env_vars() -> Token:
        token_env = os.environ.get(INITIAL_TOKEN_ENV)
        if not token_env:
            raise ValueError(
                f"You don't have any token saved on database, specify it via {INITIAL_TOKEN_ENV}"
            )
        try:
            token = json.loads(token_env)
            current_token = SpotifyToken(**token)
            current_token_ = Token(
                expires_at=0, **dict(current_token)
            )  # Make first time token expire automatically so we get a new one instantly
            return current_token_
        except JSONDecodeError as e:
            raise ValueError(
                f"Initial token on var: {INITIAL_TOKEN_ENV} is malformed. Error: {e}"
            )
        except ValidationError as e:
            raise ValueError(f"Initial token parsing was bad. Error: {e}")

    def delete_user(self, mail: Mail, token: Token) -> Result[User, Error]:
        result = self.spotify_user.delete_user(mail, token)
        if result.is_error:
            return result
        return self._delete_user_from_db(result.success)

    def _delete_user_from_db(self, user: User) -> Result[User, Error]:
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM users WHERE mail = ?", (user.mail.address,))
            self.connection.commit()

            if cursor.rowcount == 0:
                return Result(Error(message="User not found"))

            return Result(success=None)
        except sqlite3.Error as e:
            return Result(Error(message=str(e)))

    def add_user(self, mail: Mail, token: Token) -> Result[User, Error]:
        result = self.spotify_user.add_user(mail, token)
        if result.is_error:
            return result
        return self._add_user_to_db(result.success)

    def _add_user_to_db(self, user: User) -> Result[User, Error]:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO users (mail, creation_date) VALUES (?, ?)",
                (user.mail.address, user.creation_date),
            )
            self.connection.commit()
            return Result(success=user)
        except sqlite3.IntegrityError:
            return Result(Error(message="User already exists"))
        except sqlite3.Error as e:
            return Result(Error(message=str(e)))

    def users(self) -> Result[List[User], Error]:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT mail, creation_date FROM users")
            rows = cursor.fetchall()
            return Result(
                success=[
                    User(mail=Mail(address=row[0]), creation_date=row[1])
                    for row in rows
                ]
            )
        except sqlite3.Error as e:
            return Result(Error(message=str(e)))

    def refresh_token(self) -> Result[Token, Error]:
        refreshed_token_result = self.spotify_token.refresh_token()
        if refreshed_token_result.is_error:
            return refreshed_token_result
        return self._add_token_to_db(refreshed_token_result.success)

    def get_token(self) -> Result[Token, Error]:
        if res := self._get_token_from_db():
            return res
        return Result(
            error=Error("Impossible error on backend, we should allways have a token!")
        )

    def _add_token_to_db(self, token: Token) -> Result[Token, Error]:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                INSERT INTO tokens (
                    access_token, token_type, expires_in, refresh_token, scope, id_token, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    token.access_token,
                    token.token_type,
                    token.expires_in,
                    token.refresh_token,
                    token.scope,
                    token.id_token,
                    token.expires_at,
                ),
            )
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            return Result(error=Error(f"Token already exists: {e}"))
        except sqlite3.Error as e:
            return Result(error=Error(f"Error saving token inside sqlite: {e}"))

    def _get_token_from_db(self) -> Result[Token, Error] | None:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM tokens LIMIT 1")
            row = cursor.fetchone()
            if row:
                return Result(
                    success=Token(
                        access_token=row[0],
                        token_type=row[1],
                        expires_in=row[2],
                        refresh_token=row[3],
                        scope=row[4],
                        id_token=row[5],
                        expires_at=row[6],
                    )
                )
            return None
        except sqlite3.Error as e:
            return Result(error=Error(f"Error retrieving token from sqlite: {e}"))
