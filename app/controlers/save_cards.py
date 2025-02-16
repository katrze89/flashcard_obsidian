from dataclasses import asdict

from app.db.db import DB
from app.models.flashcard import FlashCardSrc
from app.settings.settings import DIRNAME


def save_cards(flashcards: list[FlashCardSrc]) -> None:
    with DB(db_dir=DIRNAME / ".store", db_file_name="flashcards") as db:
        db.create_many([asdict(card) for card in flashcards])
