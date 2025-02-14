from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path

from app.models.note_models import Note


class NotesLoaderABC(ABC):
    @property
    @abstractmethod
    def folder_path(self) -> Path:
        raise NotImplementedError

    @property
    @abstractmethod
    def tags(self) -> Iterable[str]:
        raise NotImplementedError

    @abstractmethod
    def load(self) -> list[Note]:
        raise NotImplementedError
