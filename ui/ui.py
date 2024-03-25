from datetime import datetime, timedelta
import time
from typing import Union

from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

from tasks.task_manager import TaskManager
from users.user_manager import UserManager
from tasks.task import Task
from tasks.priority import Priority
from users.user import User
import config
from config import TIME_FORMAT


console = Console()


def create_table(name : str, commands : list[Union[str, Task, User]]):
    table = Table(title=name, title_style="bold blue")
    table.add_column("Nr", style="cyan", justify="center")
    if isinstance(commands[0], Task):
        table.add_column("Description", style="magenta")
        table.add_column("Complete", style="green")
        table.add_column("Due Date", style="yellow")
        table.add_column("Priority", style="red")
        table.add_column("Create Date", style="blue")

        for i, option in enumerate(commands, 1):
            table.add_row(str(i), *option.pretty_tuple())
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

def choose_date(date: datetime = None):
    date_options = ["Minutes", "Hours", "Days", "Weeks", "Months", "Years"]
    date = date if date else datetime.now()
    date_option = Prompt.ask(f"Change date {date.strftime(TIME_FORMAT)} by", choices=date_options, default=None, show_default=False)
    if date_option is not None:
        while True:
            try:
                time = int(Prompt.ask("{0} to add".format(date_option), default=0))
                if time < 0:
                    raise ValueError("Time cannot be negative")
                break
            except ValueError as ve:
                console.print(f"[bold red]{ve}[/bold red]")

    match date_option:
        case "Minutes":
            date += timedelta(minutes=time)
        case "Hours":
            date += timedelta(hours=time)
        case "Days":
            date += timedelta(days=time)
        case "Weeks":
            date += timedelta(weeks=time)
        case "Months":
            date += timedelta(days=31 * time)
        case "Years":
            date += timedelta(days=365 * time)
        case _:
            date = datetime.strptime(Prompt.ask("Enter date", default=date.strftime(TIME_FORMAT)), TIME_FORMAT)

    return date.timestamp()

def options_menu(user_email : str):
    time.sleep(0.1)
    console.clear()
    task_manager = TaskManager(user_email)
    while True:
        console.clear()
        console.print(create_table("Commands", task_manager.commands))
        try:
            option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(TaskManager.commands) + 1)]))
            tasks_menu(task_manager, option)
        except Exception as e:
            console.print(f"[bold red]{e}[/bold red]")
            time.sleep(3)
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Logging out![/bold yellow]")
            time.sleep(3)
            break

def login_menu():
    console.print(create_table("Actions", UserManager.options))
    user_manager = UserManager()

    # Remember option
    if config.remember:
        console.print(f"[bold green]Remembered user: {config.remember_email}[/bold green]")
        try:
            options_menu(user_manager.login(config.remember_email, Prompt.ask("Password", password=True)))
            raise KeyboardInterrupt("Exiting...")
        except ValueError as ve:
            console.print(f"[bold red]{ve}[/bold red]")
            time.sleep(3)



    option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(UserManager.options) + 1)]))
    time.sleep(0.2)
    console.clear()
    try:
        match option:
            case 1:
                console.print("[bold green]Logging in![/bold green]")
                options_menu(user_manager.login(Prompt.ask("Email"), Prompt.ask("Password", password=True)))
            case 2:
                console.print("[bold blue]Creating an account![/bold blue]")
                options_menu(user_manager.save_user(Prompt.ask("Username"), Prompt.ask("Email"), Prompt.ask("Password", password=True)))
            case 3:
                raise KeyboardInterrupt("Exiting...")
    except ValueError as ve:
        console.print(f"[bold red]{ve}[/bold red]")
        time.sleep(3)
    except Exception as e:
        console.print(f"[bold red]Unknown Error: {e}[/bold red]")
        time.sleep(3)
    

def update_task(task: Task):
    description = Prompt.ask("Description", default=task.description)
    complete = Prompt.ask("Complete", choices=["True", "False"], default="True" if task.complete else "False") == "True"
    due_date = choose_date(datetime.fromtimestamp(task.due_date))
    priority = Prompt.ask("Priority", choices=Priority.LEVELS.keys(), default=str(task.priority))
    return Task(task.creator_email, description, complete, due_date, priority, task.create_date)

def fill_task(email : str):
    while True:
        try:
            description = Prompt.ask("Description")
            if not description:
                raise ValueError("Description cannot be empty")
            break
        except ValueError as ve:
            console.print(f"[bold red]{ve}[/bold red]")
            
    due_date = choose_date()
    priority_name = Prompt.ask("Priority", choices=["Low", "Medium", "High"], default="Low")

    priority = Priority(priority_name)
    try:
        task = Task(email=email, description=description, due_date=due_date, priority=priority)
        console.clear()
        console.print(f"[bold green]Task created successfully![/bold green]")
        return task
    except ValueError as ve:
        console.print(f"[bold red]{ve}[/bold red]")


def sort_filter_options():
        sort_by = Prompt.ask("Sort by", choices={"due date" : "due_date", "create date" : "create_date", "priority" : "priority"})
        filter_by = {
            "complete": Prompt.ask("Complete", choices=["True", "False", "Both"], default="Both"),
            "priority": Prompt.ask("Priority", choices=["Low", "Medium", "High", "All"], default="All"),
            "due_date": Prompt.ask("Due date", default=datetime.now().strftime(TIME_FORMAT)),
            "create_date": Prompt.ask("Create date")
        }
        return sort_by, filter_by

def tasks_menu(task_manager: TaskManager, option: int):
    console.clear()
    match option:
        case 1:
            console.print("[bold green]Creating a task![/bold green]")
            task_manager.create_task(fill_task(task_manager.email))
        case 2:
            console.print("[bold blue]Updating a task![/bold blue]")
            if task_manager.tasks == []:
                raise Exception("No tasks to update!")
            console.print(create_table("tasks", task_manager.tasks))
            task = task_manager.tasks[int(Prompt.ask("Select an task to update", choices=[str(i) for i in range(1, len(task_manager.tasks) + 1)])) - 1]
            task_manager.update_task(task, update_task(task))
        case 3:
            console.print("[bold red]Deleting a task![/bold red]")
            if task_manager.tasks == []:
                raise Exception("No tasks to delete!")
            console.print(create_table("tasks", task_manager.tasks))
            choice = int(Prompt.ask("Select an task to delete", choices=[str(i) for i in range(1, len(task_manager.tasks) + 1)], default=0)) - 1
            if choice == -1:
                raise ValueError("aborting...")
            task_manager.delete_task(task_manager.tasks[choice])
        case 4:
            console.print("[bold yellow]Listing all tasks![/bold yellow]")
            if task_manager.tasks == []:
                raise Exception("No tasks to list!")
            sort_by, filter_by = None, None  # sort_filter_options()
            tasks = task_manager.list_tasks(task_manager.tasks, sort_by=sort_by, filter_by=filter_by)
            console.print(create_table("tasks", tasks))
            Prompt.ask("Press enter to continue")
        case 5:
            raise KeyboardInterrupt("Exiting...")

def menu():
    while True:
        try:
            console.clear()
            login_menu()
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Goodbye![/bold yellow]")
            break