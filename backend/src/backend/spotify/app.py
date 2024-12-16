import time
from dataclasses import dataclass
from typing import List, Callable

from pydantic import ValidationError

from src.backend.spotify.result import Result, Error
from src.backend.spotify.domain.token_repository import (
    TokenRepository,
    Token,
)
from src.backend.spotify.domain.user_repository import (
    UserRepository,
    User,
    Mail,
)


class MailError(Error):
    pass


class FetchUsersError(Error):
    pass


class DuplicatedUserInDatabaseError(Error):
    pass


class DeletingUserError(Error):
    pass


class CreatingUserError(Error):
    pass


class TokenExpired(Error):
    pass


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
    def _found_user(user: List[User]) -> Result[User, DuplicatedUserInDatabaseError]:
        if len(user) == 1:
            return Result.success(user[0])
        return Result.failure(
            DuplicatedUserInDatabaseError(
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

    def _create_user(
        self, mail: Mail
    ) -> Result[User, CreatingUserError | TokenExpired]:
        result_token = self._get_token()
        if result_token.is_error:
            return Result.failure(
                TokenExpired(message=result_token.error_value.message)
            )
        result_creating = self.users.add_user(
            mail=mail, token=result_token.success_value
        )
        if result_creating.is_error:
            return Result.failure(
                CreatingUserError(message=result_creating.error_value.message)
            )
        return result_creating  # type: ignore

    def _delete_first_user(
        self, users: List[User]
    ) -> Result[None, DeletingUserError | TokenExpired]:
        first_user: User = min(users, key=lambda user: user.creation_date)
        token = self._get_token()
        if token.is_error:
            return Result.failure(TokenExpired(message=token.error_value.message))
        result = self.users.delete_user(first_user.mail, token.success_value)
        if result.is_error:
            return Result.failure(DeletingUserError(message=result.error_value.message))
        return Result.success(None)

    @staticmethod
    def _get_mail(mail: str) -> Result[Mail, MailError]:
        try:
            return Result.success(Mail(address=mail))
        except ValidationError:
            return Result.failure(MailError(message="Your mail is incorrect"))

    def add_user(
        self, mail: str
    ) -> Result[
        User,
        MailError
        | FetchUsersError
        | DuplicatedUserInDatabaseError
        | DeletingUserError
        | CreatingUserError
        | TokenExpired,
    ]:
        result_mail = SpotifyApp._get_mail(mail)
        if result_mail.is_error:
            return result_mail  # type: ignore
        _mail = result_mail.success_value
        users = self.users.users()
        if users.is_error:
            return Result.failure(FetchUsersError(users.error_value.message))
        user_list: List[User] = users.success_value
        user = list(filter(lambda usr: usr.mail.address == mail, user_list))
        if user:
            return SpotifyApp._found_user(user)  # type: ignore
        if len(user_list) >= self.users_threshold:
            delete_status = self._delete_first_user(user_list)
            if delete_status.is_error:
                return delete_status  # type: ignore
        return self._create_user(_mail)  # type: ignore
