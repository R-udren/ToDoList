from time import sleep
from typing import Union

from rich.console import Console
from rich.table import Table

from tasks.task import Task
from tasks.task_manager import TaskManager
from users.user import User

console = Console()


def create_table(name: str, commands: list[Union[str, Task, User]], start_from: int = 1) -> Table:
    table = Table(title=name, title_style="bold bright_blue", show_lines=True)
    table.add_column("Nr", style="bright_cyan", justify="center")
    if isinstance(commands[0], Task):  # Create Task table
        table.add_column("Description", style="magenta", overflow="fold")
        table.add_column("Complete", style="green")
        table.add_column("Due Date", style="yellow")
        table.add_column("Priority", style="red")
        table.add_column("Create Date", style="blue")

        for i, option in enumerate(commands, start_from):
            task_params = list(option.pretty_tuple())
            task_params[1] = f"[green]{task_params[1]}[/green]" if task_params[1] == "True" else f"[red]{task_params[1]}[/red]"
            if task_params[3] == "High":
                task_params[3] = f"[red]{task_params[3]}[/red]"
            elif task_params[3] == "Medium":
                task_params[3] = f"[yellow]{task_params[3]}[/yellow]"
            else:
                task_params[3] = f"[cyan]{task_params[3]}[/cyan]"
            task_params[3] = f"[bold]{task_params[3]}[/bold]"
            table.add_row(str(i), *task_params)
        return table

    elif isinstance(commands[0], User):  # Create user table
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="magenta")

        for i, option in enumerate(commands, start_from):
            table.add_row(str(i), option.email, option.username)
        return table
    else:  # Create actions table
        table.add_column("Description", style="bright_magenta")

        for i, option in enumerate(commands, start_from - 1):
            table.add_row(str(i), option)
        return table


def menu(menu_state=True, email=None, add_task=False, update_task=False, delete_task=False, mark_complete=False,
         list_tasks=False, export_tasks=False, import_tasks=False, cli=False):
    active_email = None

    from ui.login_ui import login_menu
    while True:
        try:
            active_email = login_menu(email, cli=cli)
            break
        except KeyboardInterrupt:
            console.print("[bold yellow]Exiting...[/bold yellow]")
            exit()
        except Exception as e:
            console.print(f"[bold red]{e}[/bold red]")

    if active_email and not menu_state:
        from ui.tasks_ui import tasks_menu, task_manager_menu
        option = {add_task: 1, update_task: 2, delete_task: 3, mark_complete: 4, list_tasks: 5, export_tasks: 6,
                  import_tasks: 7}.get(True, 0)
        try:
            if option <= 4:
                task_manager_menu(TaskManager(active_email), option)
            else:
                state = tasks_menu(TaskManager(active_email), option - 3)
                if state:
                    console.print(state)
                    sleep(1)
        except Exception as e:
            console.print(f"[bold red]{e}[/bold red]")
            sleep(2)
    menu_state = True

    if menu_state and active_email:
        from ui.tasks_ui import options_menu
        console.clear()
        try:
            options_menu(active_email)
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Logging out...[/bold yellow]")
            menu()

    else:
        console.print("[bold red]No options selected![/bold red]")
