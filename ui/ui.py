from datetime import datetime

from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

from tasks.task_manager import TaskManager
from users.user_manager import UserManager
from tasks.task import Task
from tasks.priority import Priority

from config import TIME_FORMAT


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
            tasks_menu(task_manager, option)
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

def fill_task(email : str):
    description = Prompt.ask("Description")
    due_date = Prompt.ask(f"Due date", default=datetime.now().strftime(TIME_FORMAT))
    priority_name = Prompt.ask("Priority", choices=["Low", "Medium", "High"], default="Low")
    priority = Priority(priority_name)
    return Task(email=email, description=description, due_date=due_date, priority=priority)

def show_tasks(tasks: list[Task]):
    table = Table(title="Tasks", title_style="bold blue")
    table.add_column("Nr", style="cyan", justify="center")
    table.add_column("Description", style="magenta")
    table.add_column("Complete", style="green")
    table.add_column("Due Date", style="yellow")
    table.add_column("Priority", style="red")
    table.add_column("Create Date", style="blue")

    for task in tasks:
        table.add_row(str(tasks.index(task) + 1), task.description, str(bool(task.complete)), task.due_date, str(Priority(task.priority)), task.create_date)
    console.print(table)


def sort_filter_options():
        sort_by = Prompt.ask("Sort by", choices={"due date" : "due_date", "create date" : "create_date", "priority" : "priority"})
        filter_by = {
            "complete": Prompt.ask("Complete", choices=["True", "False", "Both"], default="Both"),
            "priority": Prompt.ask("Priority", choices=["Low", "Medium", "High"], default="All"),
            "due_date": Prompt.ask(f"Due date", default=datetime.now().strftime(TIME_FORMAT)),
            "create_date": Prompt.ask("Create date")
        }
        return sort_by, filter_by

def tasks_menu(task_manager: TaskManager, option: int):
    match option:
        case 1:
            task_manager.create_task(fill_task(task_manager.email))
        case 2:
            task_manager.update_task(TaskManager.input_task(task_manager.email), task_manager.tasks[int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(task_manager.tasks) + 1)])) - 1])
        case 3:
            task_manager.delete_task(task_manager.tasks[int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(task_manager.tasks) + 1)])) - 1])
        case 4:
            if task_manager.records == []:
                raise Exception("No tasks to list")
            sort_by, filter_by = None, None  # sort_filter_options()
            tasks = task_manager.list_tasks(task_manager.tasks, sort_by=sort_by, filter_by=filter_by)
            show_tasks(tasks)
        case 5:
            task_manager.exit()

def menu():
    while True:
        try:
            login_menu()
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Goodbye![/bold yellow]")
            break

def exit():
    raise KeyboardInterrupt("Exiting...")