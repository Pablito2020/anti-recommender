from dataclasses import dataclass, field
from typing import TypeVar, Generic, Union, cast

T = TypeVar("T")


@dataclass(frozen=True)
class Error:
    message: str


E = TypeVar("E", bound=Error)


@dataclass(frozen=True)
class Success(Generic[T]):
    value: T


@dataclass(frozen=True)
class Failure(Generic[E]):
    value: E


@dataclass
class Result(Generic[T, E]):
    __state: Union[Success[T], Failure[E]] = field(init=False)

    @staticmethod
    def success(value: T) -> "Result[T, E]":
        result = Result.__new__(Result)
        result.__state = Success(value)
        return result

    @staticmethod
    def failure(error: E) -> "Result[T, E]":
        result = Result.__new__(Result)
        result.__state = Failure(error)
        return result

    @property
    def is_error(self) -> bool:
        return isinstance(self.__state, Failure)

    @property
    def error_value(self) -> "E":
        if self.is_error:
            return cast(E, self.__state.value)
        raise ValueError("We don't have an error! Please check if it's an error first")

    @property
    def success_value(self) -> "T":
        if not self.is_error:
            return cast(T, self.__state.value)
        raise ValueError(
            "We don't have a success value! Please check if it's a valid value first"
        )
