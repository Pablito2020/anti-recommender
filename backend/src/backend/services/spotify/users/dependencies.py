import os
from functools import wraps
from typing import TypeVar, Callable, Any

from src.backend.services.spotify.users.app import SpotifyApp
from src.backend.services.spotify.users.infra.repository_implementation import (
    RepositoryImplementation,
)

APP_ID_ENV = "APP_ID"
USER_ID_ENV = "USER_ID"
SQLITE_PATH_ENV = "SQLITE_PATH"
INITIAL_TOKEN_ENV = "INITIAL_TOKEN"

T = TypeVar("T", bound=Callable[..., Any])


def require_env_var(
    env_var_name: str, error_message: str, could_be_none: bool = False
) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> str:
            value = os.environ.get(env_var_name)
            if value is None and not could_be_none:
                raise ValueError(error_message)
            return value  # type: ignore

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


@require_env_var(
    INITIAL_TOKEN_ENV,
    f"You have to provide an initial token. Do it via env var {INITIAL_TOKEN_ENV}",
    could_be_none=True,
)
def get_initial_token_env() -> str | None:
    pass


def get_sqlite_repo() -> RepositoryImplementation:
    app_id = get_app_id()
    user_id = get_user_id()
    sqlite_path = get_sqlite_path()
    initial_token = get_initial_token_env()
    return RepositoryImplementation(
        app_id=app_id,
        user_id=user_id,
        sqlite_path=sqlite_path,
        initial_token=initial_token,
    )


sqlite_repo = get_sqlite_repo()

_spotify_app = SpotifyApp(users=sqlite_repo, tokens=sqlite_repo)


async def get_spotify_app() -> SpotifyApp:
    return _spotify_app
