from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

console = Console()

options = [
        "Create a task",
        "Update a task",
        "Delete a task",
        "List all tasks",
        "Exit"
    ]

def create_options_table():
    table = Table(title="Options", title_style="bold blue")
    table.add_column("Nr", style="cyan", justify="center")
    table.add_column("Description", style="magenta")

    for i, option in enumerate(options, 1):
        table.add_row(str(i), option)

    return table

def menu():
    console.print(create_options_table())
    option = Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(options) + 1)])

    return int(option)

if __name__ == "__main__":
    menu()