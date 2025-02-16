import re

import typer

from app.cli.cards.read import read_all_cli
from app.cli.utils import display_table
from app.controlers.read_cards import get_cards_by_id
from app.controlers.save_deck import save_deck

app = typer.Typer()


@app.command(name="create-deck")
def create_deck_cli() -> None:
    read_all_cli()
    name = typer.prompt("Enter desck name: ")
    indexes = typer.prompt("Provide list of card indexes, comma separated", type=str)
    indexes_digits = {int(digit) for digit in re.findall(r"\d+", indexes)}

    cards = get_cards_by_id(list(indexes_digits))
    display_table(
        title="flashcards_AI",
        columns={"Indexes": "id", "Question": "front_side", "level": "difficulty_level"},
        items=cards,
    )
    save_deck({"name": name, "card_idx": [card.id for card in cards]})
