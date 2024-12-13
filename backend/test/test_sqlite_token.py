import json
import os

import pytest

from backend.services.spotify.users.domain import Token
from backend.services.spotify.users.infra.sqlite.token import SqliteTokenRepository

sqlite_path = "./token-test.db"


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    os.remove(sqlite_path)


def test_if_not_token_found_throws_error():
    try:
        SqliteTokenRepository(sqlite_path=sqlite_path, initial_token=None)
        assert False, "Isn't throwing an error"
    except Exception:
        assert True, "Should throw an error"


def test_if_valid_token_is_saved():
    initial_token = '{"access_token":"test","token_type":"test","expires_in":3600,"refresh_token":"test","scope":"test","id_token":"test"}'
    valid_token = Token(expires_at=0, **(json.loads(initial_token)))
    repo = SqliteTokenRepository(sqlite_path=sqlite_path, initial_token=initial_token)
    current_token_result = repo.get_token()
    assert not current_token_result.is_error, "Should not be an error"
    assert valid_token.dict() == current_token_result.success_value.dict()


def test_if_invalid_token_return_error():
    try:
        initial_token = '{"access_token":"test","expires_in":3600,"refresh_token":"test","scope":"test","id_token":"test"}'
        SqliteTokenRepository(sqlite_path=sqlite_path, initial_token=initial_token)
        assert False, "The creation of a sqlite repository with an invalid token should throw an error"
    except Exception:
        assert True, "Should throw an error"


def test_updating_a_token():
    initial_token = '{"access_token":"test","token_type":"test","expires_in":3600,"refresh_token":"test","scope":"test","id_token":"test"}'
    repo = SqliteTokenRepository(sqlite_path=sqlite_path, initial_token=initial_token)
    new_token = Token(
        expires_at=2000,
        access_token="test2",
        token_type="test2",
        expires_in=3700,
        refresh_token="test2",
        scope="test2",
        id_token="test2",
    )
    result_adding = repo.add_token(new_token)
    result_getting = repo.get_token()
    assert not result_adding.is_error, "Should not be an error"
    assert new_token.dict() == result_adding.success_value.dict()
    assert not result_getting.is_error, "Should not be an error"
    assert new_token.dict() == result_getting.success_value.dict()
