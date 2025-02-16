# TODO add filet cards by hashtags, file
import typer

from app.cli.utils import display_table
from app.controlers.read_cards import read_all

app = typer.Typer()


@app.command(name="read-all-cards")
def read_all_cli() -> None:
    cards = read_all()
    display_table(
        title="flashcards_AI",
        columns={"Indexes": "id", "Question": "front_side", "level": "difficulty_level"},
        items=cards,
    )
