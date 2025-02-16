import re

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from app.cli.utils import display_table
from app.controlers.create_cards import create_cards
from app.controlers.read_cards import get_cards_by_id, read_all
from app.controlers.save_cards import save_cards
from app.controlers.save_deck import save_deck

app = typer.Typer(add_completion=False)

console = Console()


@app.callback(invoke_without_command=True)
def menu() -> None:
    print("Choose options:")
    print("1. Create cards for Vault")
    print("2. Get cards form DB")
    print("3. Create Deck")

    choice = typer.prompt("Provide Option number", type=int)

    match choice:
        case 1:
            cards = create_flashcards()
            save_to_db = typer.confirm("Do you want to save cards to db?")
            if save_to_db:
                save_cards_cli(cards)
        case 2:
            read_all_cli()
        case 3:
            create_deck_cli()
        case _:
            print("thank you for using FLashcards AI")


@app.command()
def create_deck_cli():
    read_all_cli()
    name = typer.prompt("Enter desck name: ")
    indexes = typer.prompt("Provide list of card indexes, comma separated", type=str)
    indexes_digits = {int(digit) for digit in re.findall(r"\d+", indexes)}

    cards = get_cards_by_id(indexes_digits)
    display_table(
        title="flashcards_AI",
        columns=("Index", "Question", "Level"),
        items=cards
    )
    # table = Table("Index", "Question", "Level", title="flashcards_AI")
    # for card in cards:
    #     table.add_row(str(card.id), card.front_side, card.difficulty_level)
    # console.print(table)

    save_deck({"name": name, "card_idx": [card.id for card in cards]})


@app.command()
def read_all_cli() -> None:
    cards = read_all()
    display_table(
        title="flashcards_AI",
        columns=("Index", "Question", "Level"),
        items=cards
    )


@app.command()
def save_cards_cli(cards) -> None:
    save_cards(cards)


@app.command()
def test() -> None:
    """
    Testing command
    """
    print("flashcards AI")


@app.command(name="create-cards")
def create_flashcards():
    """
    Create flashcards
    """
    # total = 100
    # with typer.progressbar(range(total), label = "Generating...") as progress:
    #     for _ in progress:
    #         time.sleep()
    cards = create_cards()
    table = Table("Question", "Level", title="flashcards_AI")
    for card in cards:
        table.add_row(card.front_side, card.difficulty_level.value)
    console.print(table)
    return cards
