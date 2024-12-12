from unittest.mock import MagicMock

from backend.common.result import Result, Error
from backend.services.spotify.users.app import SpotifyApp
from backend.services.spotify.users.domain import UserRepository, TokenRepository
from test.mothers.token import get_token_that_expires_on
from test.mothers.user import get_user


def test_if_user_is_already_on_db_return_it():
    mail = "added@test.com"
    user_repo: UserRepository = MagicMock()
    already_existing_user = get_user(mail)
    user_repo.users = MagicMock(return_value=(Result.success([already_existing_user])))
    token_repository = MagicMock()
    app = SpotifyApp(users=user_repo, tokens=token_repository)
    user = app.add_user(mail)
    assert not user.is_error, "Should not be an error"
    assert user.success_value == already_existing_user


def test_if_cant_fetch_users_it_fails():
    user_repo: UserRepository = MagicMock()
    user_repo.users = MagicMock(return_value=(Result.failure(Error(""))))
    token_repository = MagicMock()
    app = SpotifyApp(users=user_repo, tokens=token_repository)
    user = app.add_user("test@test.com")
    assert user.is_error, "We shouldn't add a user if we can't fetch the users"


def test_if_user_is_not_in_database_create_it():
    current_time = 100_000
    already_existing_user = get_user("added@test.com")
    new_user = get_user("nonadded@test.com", creation_date=current_time)

    user_repo: UserRepository = MagicMock()
    user_repo.users = MagicMock(return_value=(Result.success([already_existing_user])))
    user_repo.add_user = MagicMock(return_value=(Result.success(new_user)))

    def time():
        return current_time

    token_repository: TokenRepository = MagicMock()
    token = get_token_that_expires_on(current_time + 100)
    token_repository.get_token = MagicMock(return_value=(Result.success(token)))

    app = SpotifyApp(users=user_repo, tokens=token_repository, time_now=time)
    user = app.add_user("nonadded@test.com")
    assert not user.is_error, "We shouldn't have an user error"
    assert user.success_value == new_user, "We shouldn't have an user error"


def test_if_repository_add_fails_we_dont_add_user():
    current_time = 100_000
    already_existing_user = get_user("added@test.com")
    new_user = get_user("nonadded@test.com", creation_date=current_time)

    user_repo: UserRepository = MagicMock()
    user_repo.users = MagicMock(return_value=(Result.success([already_existing_user])))
    user_repo.add_user = MagicMock(return_value=(Result.failure(new_user)))

    def time() -> float:
        return current_time

    token_repository: TokenRepository = MagicMock()
    token = get_token_that_expires_on(current_time + 100)
    token_repository.get_token = MagicMock(return_value=(Result.success(token)))

    app = SpotifyApp(users=user_repo, tokens=token_repository, time_now=time)
    user = app.add_user("nonadded@test.com")
    assert user.is_error


def test_if_token_is_invalidated_and_we_refresh_it_and_get_error_we_return_error():
    current_time = 100_000
    already_existing_user = get_user("added@test.com")
    new_user = get_user("nonadded@test.com", creation_date=current_time)

    user_repo: UserRepository = MagicMock()
    user_repo.users = MagicMock(return_value=(Result.success([already_existing_user])))
    user_repo.add_user = MagicMock(return_value=(Result.success(new_user)))

    def time() -> float:
        return current_time

    token_repository: TokenRepository = MagicMock()
    token = get_token_that_expires_on(current_time - 1000)
    token_repository.get_token = MagicMock(return_value=(Result.success(token)))
    token_repository.refresh_token = MagicMock(
        return_value=(Result.failure(Error("No new token")))
    )

    app = SpotifyApp(users=user_repo, tokens=token_repository, time_now=time)
    user = app.add_user("nonadded@test.com")
    assert user.is_error


def test_if_token_is_invalidated_refresh_it_and_we_get_correct_we_add_user():
    current_time = 100_000
    already_existing_user = get_user("added@test.com")
    new_user = get_user("nonadded@test.com", creation_date=current_time)

    user_repo: UserRepository = MagicMock()
    user_repo.users = MagicMock(return_value=(Result.success([already_existing_user])))
    user_repo.add_user = MagicMock(return_value=(Result.success(new_user)))

    def time() -> float:
        return current_time

    token_repository: TokenRepository = MagicMock()
    token = get_token_that_expires_on(current_time - 1000)
    new_token = get_token_that_expires_on(current_time + 1000)
    token_repository.get_token = MagicMock(return_value=(Result.success(token)))
    token_repository.refresh_token = MagicMock(return_value=(Result.success(new_token)))

    app = SpotifyApp(users=user_repo, tokens=token_repository, time_now=time)
    user = app.add_user("nonadded@test.com")
    assert not user.is_error
    assert user.success_value == new_user
