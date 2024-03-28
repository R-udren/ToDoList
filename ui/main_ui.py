from typing import Union

from rich.console import Console
from rich.table import Table

from tasks.task_manager import TaskManager
from users.user import User
from tasks.task import Task

console = Console()


def create_table(name : str, commands : list[Union[str, Task, User]]):
    table = Table(title=name, title_style="bold blue")
    table.add_column("Nr", style="cyan", justify="center")
    if isinstance(commands[0], Task):  # Create Task table
        table.add_column("Description", style="magenta")
        table.add_column("Complete", style="green")
        table.add_column("Due Date", style="yellow")
        table.add_column("Priority", style="red")
        table.add_column("Create Date", style="blue")

        for i, option in enumerate(commands, 1):
            table.add_row(str(i), *option.pretty_tuple())
        return table

    elif isinstance(commands[0], User):  # Create user table
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="magenta")

        for i, option in enumerate(commands, 1):
            table.add_row(str(i), option.email, option.username)
        return table
    else:  # Create actions table
        table.add_column("Description", style="magenta")

        for i, option in enumerate(commands, 1):
            table.add_row(str(i), option)
        return table

def menu(menu: bool = True, email=None,
         list_tasks: bool = False, add_task: bool = False, update_task: bool = False, delete_task: bool = False, export_tasks: bool = False):
    from ui.login_ui import login_menu
    while True:
        try:
            email = login_menu(email if email else None)
            break
        except Exception as e:
            console.print(f"[bold red]{e}[/bold red]")
        except KeyboardInterrupt:
            console.print("[bold yellow]Exiting...[/bold yellow]")
            break

    if menu and email:
        from ui.tasks_ui import options_menu
        options_menu(email)
    else:
        if not email:
            console.print("[bold red]You need to login first![/bold red]")


        from ui.tasks_ui import tasks_menu
        option = {add_task: 1, update_task: 2, delete_task: 3, list_tasks: 4, export_tasks: 5}.get(True, 6)
        try:
            tasks_menu(TaskManager(email), option)
        except Exception as e:
            console.print(f"[bold red]{e}[/bold red]")
        except KeyboardInterrupt:
            console.print("[bold yellow]Exiting...[/bold yellow]")
