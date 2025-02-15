from dataclasses import dataclass
from enum import Enum


class DifficultyEnum(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class NonEmptyStr(str):
    def __new__(cls, value: str) -> "NonEmptyStr":
        if not value.strip():
            raise ValueError("Value cannot be empty")
        return super().__new__(cls, value)


@dataclass(frozen=True, kw_only=True, slots=True)
class FlashCard:
    difficulty_level: DifficultyEnum
    tags: set[NonEmptyStr]
    front_site: NonEmptyStr
    back_site: NonEmptyStr
    origin: NonEmptyStr  # name of the file based on which the question is based on
