import typer

from app.cli.utils import display_table
from app.controlers.create_cards import create_cards
from app.controlers.save_cards import save_cards
from app.models.flashcard import FlashCardSrc

app = typer.Typer()


@app.command(name="create-cards")
def reate_cards_cli() -> None:
    """
    Create flashcards from all files
    """
    cards = create_cards()
    display_table(title="flashcards_AI", columns={"Question": "front_side", "level": "difficulty_level"}, items=cards)
    save_to_db = typer.confirm("Do you want to save cards to db?")
    if save_to_db:
        save_cards_cli(cards)


# TODO change the logis so we do not check the hashtags and just create flashcards for all files


def save_cards_cli(cards: list[FlashCardSrc]) -> None:
    """
    save cards created by ChatGPT
    """
    # TODO add logic to when user are sending
    save_cards(cards)
