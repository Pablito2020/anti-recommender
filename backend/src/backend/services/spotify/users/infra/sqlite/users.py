import sqlite3
from dataclasses import dataclass
from typing import List

from src.backend.common.result import Result, Error
from src.backend.services.spotify.users.domain.user_repository import User, Mail


@dataclass
class SqliteUsersRepository:
    """
    It's a cache for our users logged in
    """

    sqlite_path: str

    def __post_init__(self) -> None:
        self._ensure_user_table()

    def _ensure_user_table(self) -> None:
        try:
            with sqlite3.connect(self.sqlite_path) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        mail TEXT PRIMARY KEY,
                        creation_date REAL NOT NULL
                    )
                    """)
                connection.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Users Database initialization error: {e}")

    def delete_user(self, user: User) -> Result[User, Error]:
        try:
            with sqlite3.connect(self.sqlite_path) as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM users WHERE mail = ?", (user.mail.address,))
                connection.commit()
                if cursor.rowcount == 0:
                    return Result.failure(Error(message="User not found"))
                return Result.success(user)
        except sqlite3.Error as e:
            return Result.failure(Error(message=str(e)))

    def add_user(self, user: User) -> Result[User, Error]:
        try:
            with sqlite3.connect(self.sqlite_path) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO users (mail, creation_date) VALUES (?, ?)",
                    (user.mail.address, user.creation_date),
                )
                connection.commit()
                return Result.success(user)
        except sqlite3.IntegrityError:
            return Result.failure(Error(message="User already exists"))
        except sqlite3.Error as e:
            return Result.failure(Error(message=str(e)))

    def users(self) -> Result[List[User], Error]:
        try:
            with sqlite3.connect(self.sqlite_path) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT mail, creation_date FROM users")
                rows = cursor.fetchall()
                return Result.success(
                    [
                        User(mail=Mail(address=row[0]), creation_date=row[1])
                        for row in rows
                    ]
                )
        except sqlite3.Error as e:
            return Result.failure(Error(message=str(e)))
