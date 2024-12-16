import json
import sqlite3
from dataclasses import dataclass
from json import JSONDecodeError

from pydantic import ValidationError

from src.backend.spotify.result import Result, Error
from src.backend.spotify.domain.token_repository import Token


@dataclass
class SqliteTokenRepository:
    sqlite_path: str
    initial_token: str | None

    def __post_init__(self) -> None:
        self._ensure_token()

    def _ensure_token(self) -> Token:
        self._ensure_token_database()
        token_from_db = self.get_token()
        if token_from_db.is_error:
            initial_token = self._get_initial_token_from_env_vars()
            result_saving = self.add_token(initial_token)
            if result_saving.is_error:
                raise ValueError("Error saving initial token to sqlite database")
            return result_saving.success_value
        return token_from_db.success_value

    def _ensure_token_database(self) -> None:
        try:
            with sqlite3.connect(self.sqlite_path) as connection:
                cursor = connection.cursor()
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
                connection.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Token Database initialization error: {e}")

    def _get_initial_token_from_env_vars(self) -> Token:
        if not self.initial_token:
            raise ValueError(
                "You don't have any token saved on database, specify it via env var"
            )
        try:
            token = json.loads(self.initial_token)
            current_token_ = Token(
                expires_at=0, **token
            )  # Make first time token expire automatically so we get a new one instantly
            return current_token_
        except JSONDecodeError as e:
            raise ValueError(
                f"Initial token json stringify value is malformed. Error: {e}"
            )
        except ValidationError as e:
            raise ValueError(f"Initial token parsing was bad. Error: {e}")

    def add_token(self, token: Token) -> Result[Token, Error]:
        try:
            with sqlite3.connect(self.sqlite_path) as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM tokens")
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
                connection.commit()
            return Result.success(token)
        except sqlite3.IntegrityError as e:
            return Result.failure(Error(f"Token already exists: {e}"))
        except sqlite3.Error as e:
            return Result.failure(Error(f"Error saving token inside sqlite: {e}"))

    def get_token(self) -> Result[Token, Error]:
        try:
            with sqlite3.connect(self.sqlite_path) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM tokens LIMIT 1")
                row = cursor.fetchone()
                if row:
                    return Result.success(
                        Token(
                            access_token=row[0],
                            token_type=row[1],
                            expires_in=row[2],
                            refresh_token=row[3],
                            scope=row[4],
                            id_token=row[5],
                            expires_at=row[6],
                        )
                    )
                return Result.failure(
                    Error("SQLITE: Can't retrieve token because it doesn't exist")
                )
        except sqlite3.Error as e:
            return Result.failure(Error(f"Error retrieving token from sqlite: {e}"))
