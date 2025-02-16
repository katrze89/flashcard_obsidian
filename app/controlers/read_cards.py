from app.db.db import DB
from app.models.flashcard import FlashCard
from app.settings.settings import DIRNAME


def read_all() -> list[FlashCard]:
    with DB(db_dir=DIRNAME / ".store", db_file_name="flashcards") as db:
        cards = db.read_all()
    return [FlashCard(**card) for card in cards]


def get_cards_by_id(ids: list[int]) -> list[FlashCard]:
    with DB(db_dir=DIRNAME / ".store", db_file_name="flashcards") as db:
        cards = db.read(ids)
    return [FlashCard(**card) for card in cards]
