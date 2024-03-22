from tasks.task import Task
from database.database_manager import DatabaseManager
from config import DB_NAME

from config import TIME_FORMAT
from datetime import datetime
from tasks.priority import Priority


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