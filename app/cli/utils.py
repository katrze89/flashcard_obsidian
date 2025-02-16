from typing import Any

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from app.controlers.create_cards import create_cards
from app.controlers.read_cards import get_cards_by_id, read_all
from app.controlers.save_cards import save_cards
from app.controlers.save_deck import save_deck

app = typer.Typer(add_completion=False)

console = Console()


def display_table(
        *,
        title: str,
        columns: tuple[str],
        items: list[Any]

):
    table = Table(*columns, title=title)
    for item in items:
        table.add_row(str(item.id), item.front_side, item.difficulty_level)
    console.print(table)