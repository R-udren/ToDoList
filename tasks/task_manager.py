from tasks.task import Task
from database_manager import DatabaseManager
from config import DB_NAME

class TaskManager:
    commands = [
        "Create a task",
        "Update a task",
        "Delete a task",
        "List all tasks",
        "Exit"
    ]

    def __init__(self):
        self.db = DatabaseManager(DB_NAME)
        self.db.create_table("tasks", ["description TEXT", "complete INTEGER", "due_date TEXT", "priority TEXT", "create_date TEXT"])
        self.tasks = self.db.read_records("tasks")


    def command(self, option: int):
        match option:
            case 1:
                task = Task()
                self.create_task(task)
            case 2:
                self.update_task()
            case 3:
                self.delete_task()
            case 4:
                self.list_tasks()
            case 5:
                self.exit()

    def create_task(self, task: Task):
        pass

    def update_task(self, old_task: Task, new_task: Task):
        pass

    def delete_task(self, task_to_delete: Task):
        pass

    def list_tasks(self, tasks: list[Task], sort_by=None, filter_by=None):
        return tasks

    def save_to_db(self, tasks: list[Task]):
        pass

    @staticmethod
    def exit():
        raise KeyboardInterrupt
