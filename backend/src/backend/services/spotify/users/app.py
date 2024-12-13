import time
from dataclasses import dataclass
from typing import List, Callable

from pydantic import ValidationError

from backend.common.result import Result, Error
from backend.services.spotify.users.domain.token_repository import (
    TokenRepository,
    Token,
)
from backend.services.spotify.users.domain.user_repository import (
    UserRepository,
    User,
    Mail,
)


@dataclass
class SpotifyApp:
    """
    This is a "hacky" class that allows adding/deleting user mails to your app
    that hasn't extension request enabled.

    We reverse engineered the code for posting and deleting users (which is just calls with your token
    to some spotify endpoints). This will eventually break the day spotify changes his API's.
    """

    users: UserRepository
    tokens: TokenRepository
    users_threshold: int = 20
    time_now: Callable[[], float] = lambda: time.time()

    @staticmethod
    def _found_user(user: List[User]) -> Result[User, Error]:
        if len(user) == 1:
            return Result.success(user[0])
        return Result.failure(
            Error(
                message=f"We have {len(user)} of your user in our database. Should be impossible"
            )
        )

    def _is_token_expired(self, token: Token) -> bool:
        is_expired = token.expires_at <= self.time_now()
        assert isinstance(is_expired, bool), "Impossible! The time library has a bug"
        return is_expired

    def _get_token(self) -> Result[Token, Error]:
        result_token = self.tokens.get_token()
        if result_token.is_error or (
            not self._is_token_expired(result_token.success_value)
        ):
            return result_token
        return self.tokens.refresh_token()

    def _create_user(self, mail: Mail) -> Result[User, Error]:
        result_token = self._get_token()
        if result_token.is_error:
            return result_token
        return self.users.add_user(mail=mail, token=result_token.success_value)

    def _delete_first_user(self, users: List[User]) -> Result[None, Error]:
        first_user: User = min(users, key=lambda user: user.creation_date)
        token = self._get_token()
        if token.is_error:
            return token
        self.users.delete_user(first_user.mail, token.success_value)
        return Result.success(None)

    @staticmethod
    def _get_mail(mail: str) -> Result[Mail, Error]:
        try:
            return Result.success(Mail(address=mail))
        except ValidationError:
            return Result.failure(Error(message="Your mail is incorrect"))

    def add_user(self, mail: str) -> Result[User, Error]:
        result_mail = SpotifyApp._get_mail(mail)
        if result_mail.is_error:
            return result_mail
        _mail = result_mail.success_value
        users = self.users.users()
        if users.is_error:
            return Result.failure(users.error_value)
        user_list: List[User] = users.success_value
        user = list(filter(lambda usr: usr.mail.address == mail, user_list))
        if user:
            return SpotifyApp._found_user(user)
        if len(user_list) >= self.users_threshold:
            delete_status = self._delete_first_user(user_list)
            if delete_status.is_error:
                return delete_status
        return self._create_user(_mail)
