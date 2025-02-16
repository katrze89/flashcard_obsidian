from typing import Any

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(add_completion=False)

console = Console()


def display_table(*, title: str, columns: dict[str, str], items: list[Any]) -> None:
    columns_name = columns.keys()
    columns_field = list(columns.values())
    table = Table(*columns_name, title=title)
    for item in items:
        row_item = (str(getattr(item, field)) for field in columns_field)
        table.add_row(*row_item)
    console.print(table)
