import typer

app = typer.Typer()


@app.command()
def version() -> None:
    print("CLI version 0.0.1")
