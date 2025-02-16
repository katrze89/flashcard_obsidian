from dataclasses import dataclass
from enum import Enum


class DifficultyEnum(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    def __str__(self) -> str:
        return self.value


class NonEmptyStr(str):
    def __new__(cls, value: str) -> "NonEmptyStr":
        if not value.strip():
            raise ValueError("Value cannot be empty")
        return super().__new__(cls, value)


@dataclass(frozen=True, kw_only=True, slots=True)
class FlashCardSrc:
    difficulty_level: DifficultyEnum
    tags: list[NonEmptyStr]
    front_side: NonEmptyStr
    back_side: NonEmptyStr
    origin: NonEmptyStr  # name of the file based on which the question is based on


@dataclass(frozen=True, kw_only=True, slots=True)
class FlashCard(FlashCardSrc):
    id: int
