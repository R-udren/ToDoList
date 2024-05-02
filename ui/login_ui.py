from rich.console import Console
from rich.prompt import Prompt

from config import PASSWORD_ATTEMPTS
from ui.main_ui import create_table
from users.user import User
from users.user_manager import UserManager

console = Console()
user_manager = UserManager()


def login_menu(user_email=None, cli=False):
    if cli:
        return login_option(user_email)
    else:
        return login_ui()


def login_ui():
    console.clear()
    console.print(create_table("Actions", UserManager.options))
    option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(len(UserManager.options))]))
    console.clear()
    try:
        match option:
            case 1:
                console.print("[bold green]Logging in![/bold green]")
                return login_option()
            case 2:
                console.print("[bold blue]Creating an account![/bold blue]")
                return create_account_option()
            case 3:
                console.print("[bold red]Deleting an account![/bold red]")
                return user_manager.delete_user(login_option())
            case 0:
                raise KeyboardInterrupt("Exiting...")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


def login_option(user_email: str = None):
    user_email = user_email or Prompt.ask("Email")
    for attempt in range(PASSWORD_ATTEMPTS):
        password = Prompt.ask("Password", password=True)
        try:
            return user_manager.login(user_email, password)
        except ValueError as ve:
            console.print(f"[bold red]{ve}, attempts remaining {PASSWORD_ATTEMPTS - attempt - 1}[/bold red]")


def create_account_option():
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
