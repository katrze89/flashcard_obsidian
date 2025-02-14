from dataclasses import dataclass
from enum import Enum


class DifficultyEnum(Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


@dataclass(frozen=False, kw_only=True, slots=True)
class FlashCard:
    difficulty_level: DifficultyEnum
    tags: list[str]
    front_site: str
    back_site: str

    def __post_init__(self) -> None:
        if not self.front_site:
            raise ValueError("Flashcard has to have a question.")
        if not self.back_site:
            raise ValueError("Flashcard has to have an answer.")
        if not self.tags:
            raise ValueError("Tags must be a non-empty set.")
