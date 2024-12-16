import os

import pytest

from src.backend.services.spotify.users.infra.sqlite.users import SqliteUsersRepository
from test.mothers.user import get_user

sqlite_path = "./users-test.db"


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    os.remove(sqlite_path)


def test_empty_db_returns_empty_users():
    user_repo = SqliteUsersRepository(sqlite_path=sqlite_path)
    users_result = user_repo.users()
    assert not users_result.is_error
    assert users_result.success_value == [], "Should have no users"


def test_adding_a_user():
    user_repo = SqliteUsersRepository(sqlite_path=sqlite_path)
    user = get_user(mail="test@test.com")
    result_adding = user_repo.add_user(user)
    assert not result_adding.is_error
    assert result_adding.success_value == user
    users_result = user_repo.users()
    assert not users_result.is_error
    assert len(users_result.success_value) == 1
    assert users_result.success_value[0] == user
