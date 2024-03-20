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
    option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(TaskManager.commands) + 1)]))

    task_manager = TaskManager(user_id)
    while True:
        try:
            task_manager.task_command(option)
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Logging out![/bold yellow]")
            break

def login_menu():
    console.print(create_options_table(UserManager.options))
    option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(UserManager.options) + 1)]))

    user_manager = UserManager()
    choice = user_manager.user_command(option)
    if choice is not None:
        if option == 1:
            options_menu(choice)

    print(f'option: {option}, choice: {choice}')
        
def menu():
    while True:
        try:
            login_menu()
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Goodbye![/bold yellow]")
            break