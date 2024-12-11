from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")
E = TypeVar("E")


@dataclass(frozen=True)
class Result(Generic[T, E]):
    success: T | None = None
    error: E | None = None

    def __post_init__(self) -> None:
        if self.success is None and self.error is None:
            raise ValueError("Result class should have at least one result!")
        if self.success is not None and self.error is not None:
            raise ValueError("Result class should have only one result!")

    @property
    def is_error(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class Error:
    message: str
