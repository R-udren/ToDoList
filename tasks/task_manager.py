from tasks.task import Task
from database.database_manager import DatabaseManager
from config import DB_NAME

from config import TIME_FORMAT
from datetime import datetime
from tasks.priority import Priority

from rich.prompt import Prompt

class TaskManager:
    commands = [
        "Create a task",
        "Update a task",
        "Delete a task",
        "List all tasks",
        "Exit"
    ]

    def __init__(self, email : str):
        self.db = DatabaseManager(DB_NAME)
        self.db.create_task_table("tasks", ["email TEXT", "description TEXT", "complete INTEGER", "due_date TEXT", "priority INTEGER", "create_date TEXT"])
        self.records = self.db.read_records("tasks", email)
        self.tasks = [Task(*record) for record in self.records]
        self.email = email


    def task_command(self, option: int):
        match option:
            case 1:
                self.create_task(TaskManager.input_task(self.email))
            case 2:
                self.update_task(TaskManager.input_task(self.email), self.tasks[int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(self.tasks) + 1)])) - 1])
            case 3:
                self.delete_task(self.tasks[int(Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(self.tasks) + 1)])) - 1])
            case 4:
                if self.tasks == []:
                    raise Exception("No tasks to list")
                return self.tasks
                # sort_by, filter_by = TaskManager.list_options()
                # self.list_tasks(self.tasks, sort_by=sort_by, filter_by=filter_by)
            case 5:
                self.exit()

    def create_task(self, task: Task):
        self.tasks.append(task)
        self.db.add_record('tasks', [task.creator_email, task.description, task.complete, task.due_date, task.priority, task.create_date])

    def update_task(self, new_task: Task, old_task: Task):
        for (i, task) in enumerate(self.tasks):
            if task == old_task:
                self.tasks[i] = new_task
                self.db.clear_table('tasks', self.email)
                self.save_to_db()
                break
        

    def delete_task(self, task_to_delete: Task):
        self.tasks.remove(task_to_delete)
        self.db.clear_table('tasks', self.email)
        self.save_to_db()

    def list_tasks(self, tasks: list[Task], sort_by=None, filter_by=None) -> list[Task]:
        return Task.compare(tasks, sort_by, filter_by) if sort_by or filter_by else tasks

    def save_to_db(self):
        for task in self.tasks:
            self.db.add_record('tasks', [self.email, task.description, task.complete, task.due_date, task.priority, task.create_date])
    
    def list_options():
        sort_by = Prompt.ask("Sort by", choices={"due date" : "due_date", "create date" : "create_date", "priority" : "priority"})
        filter_by = {
            "complete": Prompt.ask("Complete", choices=["True", "False"]),
            "priority": Prompt.ask("Priority", choices=["Low", "Medium", "High"]),
            "due_date": Prompt.ask(f"Due date ({TIME_FORMAT})"),
            "create_date": Prompt.ask("Create date")
        }
        return sort_by, filter_by
    
    def input_task(email : str):
        description = Prompt.ask("Description")
        due_date = Prompt.ask(f"Due date", default=datetime.now().strftime(TIME_FORMAT))
        priority_name = Prompt.ask("Priority", choices=["Low", "Medium", "High"], default="Low")
        priority = Priority(priority_name)
        return Task(email=email, description=description, due_date=due_date, priority=priority)


    @staticmethod
    def exit():
        raise KeyboardInterrupt
