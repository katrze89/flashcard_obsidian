from app.db.db import DB
from app.settings.settings import DIRNAME


def save_deck(deck: dict[str, str | list[int]]) -> None:
    with DB(db_dir=DIRNAME / ".store", db_file_name="decks") as db:
        db.create(deck)
