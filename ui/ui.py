from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

from tasks.task_manager import TaskManager
from users.user_manager import UserManager


console = Console()


def create_options_table(commands : list[str]):
    table = Table(title="Options", title_style="bold blue")
    table.add_column("Nr", style="cyan", justify="center")
    table.add_column("Description", style="magenta")

    for i, option in enumerate(commands, 1):
        table.add_row(str(i), option)

    return table

def options_menu(user_id : str):
    console.print(create_options_table(TaskManager.commands))
    task_manager = TaskManager(user_id)
    while True:
        try:
            option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(TaskManager.commands) + 1)]))
            task_manager.task_command(option)
        except Exception as e:
            console.print(f"[bold red]{e}[/bold red]")
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Logging out![/bold yellow]")
            break

def login_menu():
    console.print(create_options_table(UserManager.options))
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