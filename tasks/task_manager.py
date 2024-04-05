from database.database_manager import DatabaseManager
from tasks.task import Task
from datetime import datetime

from config import DB_NAME, CSV_NAME, TIME_FORMAT

class TaskManager:
    commands = [
        "Exit",
        "Create a task",
        "Update a task",
        "Delete a task",
        "List all tasks",
        "Export to CSV",
        "Import from CSV"
    ]

    def __init__(self, email : str):
        self.db = DatabaseManager(DB_NAME)
        self.db.create_task_table("tasks", ["email TEXT", "description TEXT", "complete INTEGER", "due_date REAL", "priority INTEGER", "create_date REAL"])
        self.records = self.db.read_records("tasks", email)
        self.tasks = [Task(*record) for record in self.records]
        self.email = email

    def create_task(self, task: Task):
        self.tasks.append(task)
        self.db.add_record('tasks', list(task))

    def update_task(self, old_task: Task, new_task: Task):
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

    def sort_tasks(self, tasks: list[Task], sort_by=None, reversed=False) -> list[Task]:
        return Task.compare(tasks=tasks, sort_by=sort_by, reversed=reversed) if sort_by else tasks
    
    def search_tasks(self, tasks: list[Task], filter_by: dict) -> list[Task]:
        return Task.search(tasks, filter_by) if filter_by else tasks

    def save_to_db(self):
        for task in self.tasks:
            self.db.add_record('tasks', list(task))

    def export_tasks(self, csv_name: str=CSV_NAME):
        with open(csv_name, 'w') as file:
            for task in self.tasks:
                file.write(task.csv() + '\n')
    
    def import_tasks(self, csv_name: str=CSV_NAME):
        with open(csv_name, 'r') as file:
            for line in file:
                task = line.strip().split(',')
                task[1] = task[1] == 'True'	# Convert complete to boolean
                task[2] = datetime.strptime(task[2], TIME_FORMAT).timestamp() # Convert due_date to timestamp
                task[4] = datetime.strptime(task[4], TIME_FORMAT).timestamp() # Convert create_date to timestamp
                if not self.task_exists(task[4]):
                    ttask = Task(self.email, task[0], task[1], task[2], task[3], task[4])
                    self.tasks.append(ttask)
                    
                    self.db.add_record('tasks', list(ttask))

    def task_exists(self, create_date):
        for task in self.tasks:
            if task.create_date == create_date:
                return True
        return False