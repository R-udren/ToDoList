import time

from rich.prompt import Prompt
from rich.console import Console

from users.user_manager import UserManager
from main_ui import create_table

console = Console()

def login_menu(user_email = None):
    console.print(create_table("Actions", UserManager.options))
    user_manager = UserManager()

    option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(UserManager.options) + 1)]))
    time.sleep(0.2)
    console.clear()
    try:
        match option:
            case 1:
                console.print("[bold green]Logging in![/bold green]")
                if user_email is None:
                    user_email = Prompt.ask("Email")
                password = Prompt.ask("Password", password=True)
                return user_manager.login(user_email, password)
            case 2:
                console.print("[bold blue]Creating an account![/bold blue]")
                return user_manager.save_user(Prompt.ask("Username"), Prompt.ask("Email"), Prompt.ask("Password", password=True))
            case 3:
                raise KeyboardInterrupt("Exiting...")



    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        time.sleep(1)

def login():
    while True:
            try:
                console.clear()
                login_menu()
            except KeyboardInterrupt:
                console.print("\n[bold yellow]Goodbye![/bold yellow]")
                break