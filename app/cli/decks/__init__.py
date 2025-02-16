import typer

from app.cli.cards.create import app as create_app
from app.cli.cards.delete import app as delete_app
from app.cli.cards.read import app as read_app
from app.cli.cards.update import app as update_app

app = typer.Typer()
app.add_typer(create_app)
app.add_typer(read_app)
app.add_typer(update_app)
app.add_typer(delete_app)
