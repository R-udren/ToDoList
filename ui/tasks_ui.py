import time
from datetime import datetime, timedelta

from rich.prompt import Prompt
from rich.console import Console

from tasks.task_manager import TaskManager
from tasks.task import Task
from tasks.priority import Priority
from ui.main_ui import create_table
from config import TIME_FORMAT, CSV_NAME

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

def fill_task(email: str):
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

def filter_tasks(task_manager: TaskManager) -> list[Task]:
    attributes = ["Complete", "Priority", "Due date", "Create date"]
    filter_by = {}
    while True:
        console.clear()
        unused_attributes = [attribute for attribute in attributes if attribute not in filter_by.keys()]
        if unused_attributes == []:
            console.print("[bold orange]No more filters to add![/bold orange]")
            break
        category = Prompt.ask("Filter by", choices=unused_attributes)
        match category:
            case "Complete":
                filter_by["Complete"] = Prompt.ask("Complete", choices=["True", "False"], default="False") == "True"
            case "Priority":
                filter_by["Priority"] = Prompt.ask("Priority", choices=["Low", "Medium", "High"], default="High")
            case "Due date":
                date_options = ["Days", "Weeks", "Months", "Years"]
                date_option = Prompt.ask("Change date by", choices=date_options, default="Days", show_default=False)
                time = int(Prompt.ask(f"{date_option} to add", default="0", show_default=False))
                filter_by["Due date"] = date_option + " " + str(time)
            case "Create date":
                date_options = ["Days", "Weeks", "Months", "Years"]
                date_option = Prompt.ask("Change date by", choices=date_options, default="Days", show_default=False)
                time = int(Prompt.ask(f"{date_option} to add", default="0", show_default=False))
                filter_by["Create date"] = date_option + " " + str(time)
        if Prompt.ask("Add another filter?", choices=["Yes", "No"], default="No") == "No":
            break
    return task_manager.search(task_manager.tasks, filter_by)

def sort_tasks(task_manager: TaskManager):
    sort_by = Prompt.ask("Sort by", choices=["due_date", "create_date", "priority"], default="priority")
    reverse = Prompt.ask("What order should it be?", choices=["Ascending", "Descending"], default="Descending") == "Descending"
    return task_manager.compare(task_manager.tasks, sort_by=sort_by, reversed=reverse)

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
    match option:
        case 1:
            console.print(create_table("Actions", TaskManager.commandsM))
            option = Prompt.ask("Select an option", choices=[str(i) for i in range(len(TaskManager.commandsM))])
            task_manager_menu(task_manager, int(option))
        case 2:
            console.print("[bold yellow]Listing all tasks![/bold yellow]")
            if task_manager.tasks == []:
                raise Exception("No tasks to list!")

            sort_or_search = ["Sort", "Filter", "Both"]
            console.print(create_table("Tasks", sort_or_search, start_from=2))  # TODO: Fix this
            category = Prompt.ask("Sort or Filter", choices=[str(i) for i in range(1, len(sort_or_search) + 1)], default="Skip")
            if category != "Skip":
                category = sort_or_search[int(category) - 1]

            if category == "Sort":
                tasks = sort_tasks(task_manager)
            elif category == "Filter":
                tasks = filter_tasks(task_manager)
            elif category == "Both":
                tasks = filter_tasks(task_manager)
                tasks = sort_tasks(task_manager)
            else:
                tasks = task_manager.tasks

            if tasks != []:
                console.print(create_table("Tasks", tasks))
            else:
                console.print("[bold violet]No tasks found![/bold violet]")
            if category != "Skip":
                console.print(f"[yellow][bold]{len(task_manager.tasks) - len(tasks)}[/bold][bright_yellow] tasks skipped!")
            Prompt.ask("[cyan]Press [bold]Enter[/bold] to continue[cyan]")
        case 3:
            try:
                task_manager.export_tasks(csv_name=Prompt.ask("Enter CSV name", default=CSV_NAME))
            except Exception as e:
                console.print(f"[bold red]{e}[/bold red]")
            except KeyboardInterrupt:
                console.print("\n[bold yellow]Aborting...[/bold yellow]")
        case 4:
            try:
                task_manager.import_tasks(csv_name=Prompt.ask("Enter CSV name", default=CSV_NAME))
            except Exception as e:
                console.print(f"[bold red]{e}[/bold red]")
            except KeyboardInterrupt:
                console.print("\n[bold yellow]Aborting...[/bold yellow]")
        case 0:
            raise KeyboardInterrupt("Exiting...")
        
def task_manager_menu(task_manager: TaskManager, option: int):
    console.clear()
    match option:
        case 1:
            console.print("[bold green]Creating a task![/bold green]")
            task_manager.create_task(fill_task(task_manager.email))
        case 2:
            console.print("[bold blue]Updating a task![/bold blue]")
            if task_manager.tasks == []:
                raise Exception("No tasks to update!")
            console.print(create_table("Tasks", task_manager.tasks))
            task = task_manager.tasks[int(Prompt.ask("Select an task to update", choices=[str(i) for i in range(1, len(task_manager.tasks) + 1)])) - 1]
            task_manager.update_task(task, update_task(task))
        case 3:
            console.print("[bold red]Deleting a task![/bold red]")
            if task_manager.tasks == []:
                raise Exception("No tasks to delete!")
            console.print(create_table("Tasks", task_manager.tasks))
            choice = int(Prompt.ask("Select an task to delete [gray](To abort input nothing!)[/gray]", choices=[str(i) for i in range(1, len(task_manager.tasks) + 1)], default=0)) - 1
            if choice == -1:
                raise ValueError("aborting...")
            task_manager.delete_task(task_manager.tasks[choice])
        case 4:
            console.print("[bold yellow]Marking a task as complete![/bold yellow]")
            tasks = task_manager.search(task_manager.tasks, {"complete": False})
            if task_manager.tasks == [] or tasks == []:
                raise Exception("No tasks to mark as complete!")
            console.print(create_table("Tasks", tasks))
            choice = int(Prompt.ask("Select an task to mark as complete [gray](To abort input nothing!)[/gray]", choices=[str(i) for i in range(1, len(tasks) + 1)], default=0)) - 1
            if choice != -1:
                task_manager.mark_complete(tasks[choice])
        case 0:
            pass
    console.clear()

def options_menu(user_email: str):
    time.sleep(0.1)
    console.clear()
    task_manager = TaskManager(user_email)
    while True:
        console.clear()
        console.print(create_table("Commands", task_manager.commandsV))
        try:
            option = int(Prompt.ask("Select an option", choices=[str(i) for i in range(len(TaskManager.commandsV))]))
            console.clear()
            tasks_menu(task_manager, option)
        except Exception as e:
            console.print(f"[bold red]{e}[/bold red]")
            time.sleep(1)