import logging.config
import os
from pprint import pprint
from pathlib import Path

from app.ai.card_gen import CardGen
from app.logging_setup import logging_setup
from app.notes_reader.notes_loader import MarkdownNotesLoader

# import json

logger = logging.getLogger(__name__)


def main() -> None:
    logging_setup()
    vault_path = Path(__file__).parent.resolve() / "app/obsidian_vault"
    notes_loader = MarkdownNotesLoader(vault_path, {"python", "docker", "pytest"})
    notes = notes_loader.load()

    client_ai = CardGen(model="gpt-4o-mini")

    cards = []
    for note in [notes[0]]:
        flashcards = client_ai.create_flashcard_json(note.content)
        cards.append(flashcards.choices[0].message.content)

    pprint(cards)


if __name__ == "__main__":
    main()
