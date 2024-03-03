from rich import print  # pip install rich
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.progress import track
from rich.syntax import Syntax
import time

from test import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    recherchemot()
    # menu_automate('crédits')
    console = Console(color_system="windows")
    console.print("[bold red]Texte en rouge[/bold red]")
    console.print(console.color_system)
    console.print("[green]Texte en vert[/green]")

    console.print("[bold]Texte en gras[/bold]")
    console.print("[italic]Texte en italique[/italic]")
    console.print("[underline]Texte souligné[/underline]")

    console = Console()
    console.print("Texte aligné à gauche", justify="left")
    console.print("Texte aligné au centre", justify="center")
    console.print("Texte aligné à droite", justify="right")

    console = Console()
    table = Table(title="Exemple de tableau")
    table.add_column("Entré/Sortie", justify="left", style="cyan", no_wrap=True)
    table.add_column("Etats", justify="right", style="magenta")
    table.add_column("a", justify="right", style="magenta")
    table.add_column("b", justify="right", style="magenta")
    table.add_row("Sortie", " J'ai pas d'idéée", "a", "b")
    table.add_row("Entrée", "JH'", "b", "a")
    console.print(table)

    for i in track(range(20), description="Processing..."):
        time.sleep(1)  # Simulate work being done

    code = "for i in range(10):\n    print(i)"
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    print(syntax)

    from rich import print

    print("[image]https://www.codedex.io/images/codedex-bot-logo.gif[/image]")

    menu_automate("help")
    x = 0
    while True:
        x += 1
