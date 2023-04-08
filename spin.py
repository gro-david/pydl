from rich.console import Console
import time

console = Console()
with console.status("[bold green]Downloading...[/bold green]", spinner="aesthetic"):
    time.sleep(5)