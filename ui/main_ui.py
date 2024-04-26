from typing import Union
from time import sleep

from rich.console import Console
from rich.table import Table

from tasks.task_manager import TaskManager
from users.user import User
from tasks.task import Task

console = Console()


def create_table(name: str, commands: list[Union[str, Task, User]], start_from: int = 1) -> Table:
    table = Table(title=name, title_style="bold blue", show_lines=True)
    table.add_column("Nr", style="cyan", justify="center")
    if isinstance(commands[0], Task):  # Create Task table
        table.add_column("Description", style="magenta", overflow="fold")
        table.add_column("Complete", style="green")
        table.add_column("Due Date", style="yellow")
        table.add_column("Priority", style="red")
        table.add_column("Create Date", style="blue")

        for i, option in enumerate(commands, start_from):
            task_params = list(option.pretty_tuple())
            task_params[1] = f"[green]{task_params[1]}[/green]" if task_params[1] == "True" else f"[red]{task_params[1]}[/red]"
            task_params[3] = f"[red bold]{task_params[3]}[/red bold]" if task_params[3] == "High" else f"[cyan]{task_params[3]}[/cyan]"
            table.add_row(str(i), *task_params)
        return table

    elif isinstance(commands[0], User):  # Create user table
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="magenta")

        for i, option in enumerate(commands, start_from):
            table.add_row(str(i), option.email, option.username)
        return table
    else:  # Create actions table
        table.add_column("Description", style="magenta")

        for i, option in enumerate(commands, start_from - 1):
            table.add_row(str(i), option)
        return table

def menu(menu=True, email=None, add_task=False, update_task=False, delete_task=False, mark_complete=False, list_tasks=False, export_tasks=False, import_tasks=False):
    active_email = None
    
    from ui.login_ui import login_menu
    while True:
        try:
            active_email = login_menu(email)
            break
        except KeyboardInterrupt:
            console.print("[bold yellow]Exiting...[/bold yellow]")
            exit()
        except Exception as e:
            console.print(f"[bold red]{e}[/bold red]")
    

    if menu and active_email:
        from ui.tasks_ui import options_menu
        console.clear()
        try:
            options_menu(active_email)
        except KeyboardInterrupt:
            console.print("[bold yellow]Logging out...[/bold yellow]")
            sleep(1)

    elif active_email:
        from ui.tasks_ui import tasks_menu, task_manager_menu
        option = {add_task: 1, update_task: 2, delete_task: 3, mark_complete: 4, list_tasks: 5, export_tasks: 6, import_tasks: 7}.get(True, 0) # FIXME: Doesn't work as expected
        try:
            if option <= 4:
                task_manager_menu(TaskManager(active_email), option)
            else:
                tasks_menu(TaskManager(email), option - 3)
        except Exception as e:
            console.print(f"[bold red]{e}[/bold red]")
        except KeyboardInterrupt:
            console.print("[bold yellow]Logging out...[/bold yellow]")
            sleep(1)
            
    else:
        console.print("[bold red]No options selected![/bold red]")


                