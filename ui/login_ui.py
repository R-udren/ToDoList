import time

from rich.prompt import Prompt
from rich.console import Console

from users.user_manager import UserManager
from ui.main_ui import create_table
from config import PASSWORD_ATTEMPTS

console = Console()

def login_menu(user_email=None, password_attempts=PASSWORD_ATTEMPTS):
    user_manager = UserManager()
    if user_email:  # If called from CLI
        attempts = 0
        while password_attempts == -1 or attempts < password_attempts:
            password = Prompt.ask("Password", password=True)
            try:
                return user_manager.login(user_email, password)
            except ValueError as ve:
                console.print(f"[bold red]{ve}[/bold red]")
            attempts += 1
        console.print("[bold red]Too many attempts![/bold red]")


    console.print(create_table("Actions", UserManager.options))
    option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(UserManager.options) + 1)]))
    time.sleep(0.2)
    console.clear()
    try:
        match option:
            case 1:
                console.print("[bold green]Logging in![/bold green]")
                user_email = Prompt.ask("Email")
                for attempt in range(PASSWORD_ATTEMPTS):
                    password = Prompt.ask("Password", password=True)
                    try:
                        return user_manager.login(user_email, password)
                    except ValueError as ve:
                        console.print(f"[bold red]{ve}, attempts remaining {PASSWORD_ATTEMPTS-attempt-1}[/bold red]")
            case 2:
                console.print("[bold blue]Creating an account![/bold blue]")
                return user_manager.save_user(Prompt.ask("Username"), Prompt.ask("Email"), Prompt.ask("Password", password=True))
            case 3:
                raise KeyboardInterrupt("Exiting...")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        time.sleep(1)