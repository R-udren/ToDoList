
from rich.prompt import Prompt
from rich.console import Console

from users.user_manager import UserManager
from users.user import User
from ui.main_ui import create_table
from config import PASSWORD_ATTEMPTS

console = Console()
user_manager = UserManager()

def login_menu(user_email=None, password_attempts=PASSWORD_ATTEMPTS):
    if user_email:  # If called from CLI
        return login_cli(user_email, password_attempts)
    else:
        return login_ui()

def login_cli(user_email, password_attempts):
    attempts = 0
    while password_attempts == -1 or attempts < password_attempts:
        password = Prompt.ask("Password", password=True)
        try:
            return user_manager.login(user_email, password)
        except ValueError as ve:
            console.print(f"[bold red]{ve}[/bold red]")
        attempts += 1
    console.print("[bold red]Too many attempts![/bold red]")

def login_ui():
    console.print(create_table("Actions", UserManager.options))
    option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(len(UserManager.options))]))
    console.clear()
    try:
        match option:
            case 1:
                return login_option()
            case 2:
                return create_account_option()
            case 0:
                raise KeyboardInterrupt("Exiting...")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

def login_option():
    console.print("[bold green]Logging in![/bold green]")
    user_email = Prompt.ask("Email")
    for attempt in range(PASSWORD_ATTEMPTS):
        password = Prompt.ask("Password", password=True)
        try:
            return user_manager.login(user_email, password)
        except ValueError as ve:
            console.print(f"[bold red]{ve}, attempts remaining {PASSWORD_ATTEMPTS-attempt-1}[/bold red]")

def create_account_option():
    console.print("[bold blue]Creating an account![/bold blue]")
    username = Prompt.ask("Username")
    while True:
        email = Prompt.ask("Email")
        if User.is_email_correct(email):
            break
        console.print("[bold red]Email is not valid![/bold red]")
    while True:
        password = Prompt.ask("Password", password=True)
        if User.is_password_correct(password):
            break
        console.print("[bold red]Password is not valid![/bold red]")
    while True:
        confirm_password = Prompt.ask("Confirm Password", password=True)
        if password == confirm_password:
            break
        console.print("[bold red]Passwords do not match![/bold red]")
    try:
        return user_manager.save_user(username, email, password)
    except ValueError as ve:
        console.print(f"[bold red]{ve}[/bold red]")