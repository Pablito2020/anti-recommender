from abc import abstractmethod, ABC
from typing import List

from pydantic import BaseModel, EmailStr

from src.backend.common.result import Result, Error
from src.backend.services.spotify.users.domain.token_repository import Token


class Mail(BaseModel):
    address: EmailStr


class User(BaseModel):
    mail: Mail
    creation_date: float


class UserRepository(ABC):
    @abstractmethod
    def users(self) -> Result[List[User], Error]:
        raise NotImplementedError("Abstract class should implement fetching users")

    @abstractmethod
    def delete_user(self, mail: Mail, token: Token) -> Result[User, Error]:
        raise NotImplementedError("Abstract class should implement delete_user")

    @abstractmethod
    def add_user(self, mail: Mail, token: Token) -> Result[User, Error]:
        raise NotImplementedError("Abstract class should implement add_user")
