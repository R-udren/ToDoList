from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from typing import Union

from tasks.task_manager import TaskManager
from users.user_manager import UserManager
from tasks.task import Task
from users.user import User


console = Console()


def create_table(name : str, commands : list[Union[str, Task, User]]):
    table = Table(title=name, title_style="bold blue")
    table.add_column("Nr", style="cyan", justify="center")
    if isinstance(commands[0], Task):
        table.add_column("Description", style="magenta")
        table.add_column("Complete", style="magenta")
        table.add_column("Due Date", style="magenta")
        table.add_column("Priority", style="magenta")
        table.add_column("Create Date", style="magenta")

        for i, option in enumerate(commands, 1):
            table.add_row(str(i), option.description, str(option.complete), str(option.due_date), str(option.priority), str(option.create_date))
        return table
    elif isinstance(commands[0], User):
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="magenta")

        for i, option in enumerate(commands, 1):
            table.add_row(str(i), option.email, option.username)
        return table
    else:
        table.add_column("Description", style="magenta")

        for i, option in enumerate(commands, 1):
            table.add_row(str(i), option)
        return table

def options_menu(user_id : str):
    console.print(create_table("Actions", TaskManager.commands))
    task_manager = TaskManager(user_id)
    while True:
        try:
            option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(TaskManager.commands) + 1)]))
            if option == 4:
                console.print(create_table("Tasks", task_manager.task_command(option)))
            task_manager.task_command(option)
            
        except Exception as e:
            console.print(f"[bold red]{e}[/bold red]")
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Logging out![/bold yellow]")
            break

def login_menu():
    console.print(create_table("Actions", UserManager.options))
    user_manager = UserManager()

    option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(UserManager.options) + 1)]))
    try:
        match option:
            case 1:
                options_menu(user_manager.login(Prompt.ask("Email"), Prompt.ask("Password", password=True)))
            case 2:
                options_menu(user_manager.save_user(Prompt.ask("Username"), Prompt.ask("Email"), Prompt.ask("Password", password=True)))
            case 3:
                user_manager.exit()
    except ValueError as ve:
        console.print(f"[bold red]{ve}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Unknown Error: {e}[/bold red]")

def menu():
    while True:
        try:
            login_menu()
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Goodbye![/bold yellow]")
            break