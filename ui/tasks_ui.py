import time
from datetime import datetime, timedelta

from rich.prompt import Prompt
from rich.console import Console

from tasks.task_manager import TaskManager
from tasks.task import Task
from tasks.priority import Priority
from ui.main_ui import create_table
from config import TIME_FORMAT

console = Console()

def choose_date(date: datetime = None):
    date_options = ["Days", "Weeks", "Months", "Years"]
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
            choice = int(Prompt.ask("Select an task to delete (To abort input nothing!)", choices=[str(i) for i in range(1, len(task_manager.tasks) + 1)], default=0)) - 1
            if choice == -1:
                raise ValueError("aborting...")
            task_manager.delete_task(task_manager.tasks[choice])
        case 4:
            console.print("[bold yellow]Listing all tasks![/bold yellow]")
            if task_manager.tasks == []:
                raise Exception("No tasks to list!")
            category = Prompt.ask("Sort or search", choices=["Sort", "Filter"], default="None")

            if category == "Sort":
                sort_by = Prompt.ask("Sort by", choices={"Due date" : "due_date", "Create date" : "create_date", "Priority" : "priority"}, default="priority")
                reverse = Prompt.ask("What order should it be?", choices=["Ascending", "Descending"], default="Descending") == "Descending"
                tasks = task_manager.sort_tasks(task_manager.tasks, sort_by=sort_by, reversed=reverse)
                
            elif catagory == "Filter":
                catagory = Prompt.ask("Sort or search", choices=["Complete", "Priority", "Due date", "Create date"])
                match catagory:
                    case "complete":
                        filter_by = {
                            "complete": Prompt.ask("Complete", choices=["True", "False", "Both"], default="Both")
                        }
                    case "priority":
                        filter_by = {
                            "priority": Prompt.ask("Priority", choices=["Low", "Medium", "High", "All"], default="All")
                        }
                    case "due date":
                        date_options = ["Days", "Weeks", "Months", "Years"]
                        date_option = Prompt.ask("Change date by", choices=date_options, default="Days", show_default=False)
                        time = int(Prompt.ask("{0} to add".format(date_option), default="0", show_default=False))
                        filter_by = {
                            "due date": date_option + " " + str(time)

                        }
                    case "create date":
                        date_options = ["Days", "Weeks", "Months", "Years"]
                        date_option = Prompt.ask("Change date by", choices=date_options, default="Days", show_default=False)
                        time = int(Prompt.ask("{0} to add".format(date_option), default="0", show_default=False))
                        filter_by = {
                            "create_date": date_option + " " + str(time)
                        }
                tasks = task_manager.search_tasks(task_manager.tasks, filter_by)
            else:
                tasks = task_manager.tasks

            console.print(create_table("tasks", tasks))
            Prompt.ask("[cyan]Press [bold]Enter[/bold] to continue[cyan]")
        case 5:
            raise KeyboardInterrupt("Exiting...")

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
            time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Logging out![/bold yellow]")
            time.sleep(1)
            break