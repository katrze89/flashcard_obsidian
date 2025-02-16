import typer
from rich import print

from app.cli.cards import app as cards_app
from app.cli.cards.create import reate_cards_cli
from app.cli.cards.read import read_all_cli
from app.cli.decks import app as decks_app
from app.cli.decks.create import create_deck_cli
from app.cli.version import app as version_app

app = typer.Typer(add_completion=False)

app.add_typer(version_app)
app.add_typer(cards_app)
app.add_typer(decks_app)


@app.callback(invoke_without_command=True)
def menu() -> None:
    print("""Choose options:\n
        1. Create cards for Vault\n
        2. Get cards form DB\n
        3. Create Deck\n
    """)

    choice = typer.prompt("Provide Option number", type=int)

    match choice:
        case 1:
            reate_cards_cli()
        case 2:
            read_all_cli()
        case 3:
            create_deck_cli()
        case _:
            print("thank you for using FLashcards AI")
