from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

from tasks.task_manager import TaskManager
from tasks.task import Task


console = Console()


def create_options_table():
    table = Table(title="Options", title_style="bold blue")
    table.add_column("Nr", style="cyan", justify="center")
    table.add_column("Description", style="magenta")

    for i, option in enumerate(TaskManager.commands, 1):
        table.add_row(str(i), option)

    return table

def options_menu():
    console.print(create_options_table())
    option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(TaskManager.commands) + 1)]))

    task_manager = TaskManager()
    task_manager.command(option)


def create_task():
    description = Prompt.ask("Description")
    due_date = Prompt.ask("Due date")
    priority = Prompt.ask("Priority")
    task = Task(description, due_date, priority)
    return task


def list_options():
    sort_by = Prompt.ask("Sort by", choices=["due_date", "create_date", "priority"])
    filter_by = {
        "complete": Prompt.ask("Complete", choices=["True", "False"]),
        "priority": Prompt.ask("Priority", choices=["Low", "Medium", "High"]),
        "due_date": Prompt.ask("Due date"),
        "create_date": Prompt.ask("Create date")
    }
    return sort_by, filter_by


def menu():
    while True:
        try:
            options_menu()
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Goodbye![/bold yellow]")
            break