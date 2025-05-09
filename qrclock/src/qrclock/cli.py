"""Console script for qrclock."""
from qrclock import qrapp
import dash
import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command(name='qrclock')
def main():
    app = qrapp(debug=False)
    app.run()


if __name__ == "__main__":
    app()
