import os
from functools import wraps
from typing import TypeVar, Callable, Any

from backend.services.spotify.users.app import SpotifyApp
from backend.services.spotify.users.infra.sqlite import SqliteSpotifyRepository

APP_ID_ENV = "APP_ID"
USER_ID_ENV = "USER_ID"
SQLITE_PATH_ENV = "SQLITE_PATH"

T = TypeVar("T", bound=Callable[..., Any])


def require_env_var(env_var_name: str, error_message: str) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> str:
            value = os.environ.get(env_var_name)
            if value is None:
                raise ValueError(error_message)
            return value

        return wrapper  # type: ignore

    return decorator


@require_env_var(
    APP_ID_ENV, f"You have to provide the app_id. Do it via env var: {APP_ID_ENV}"
)
def get_app_id() -> str:  # type: ignore
    pass


@require_env_var(
    USER_ID_ENV, f"You have to provide the user_id. Do it via env var {USER_ID_ENV}"
)
def get_user_id() -> str:  # type: ignore
    pass


@require_env_var(
    SQLITE_PATH_ENV,
    f"You have to provide the sqlite path. Do it via env var {SQLITE_PATH_ENV}",
)
def get_sqlite_path() -> str:  # type: ignore
    pass


def get_sqlite_repo() -> SqliteSpotifyRepository:
    app_id = get_app_id()
    user_id = get_user_id()
    sqlite_path = get_sqlite_path()
    return SqliteSpotifyRepository(
        app_id=app_id,
        user_id=user_id,
        sqlite_path=sqlite_path,
    )


sqlite_repo = get_sqlite_repo()

_spotify_app = SpotifyApp(users=sqlite_repo, tokens=sqlite_repo)


async def get_spotify_app() -> SpotifyApp:
    return _spotify_app
