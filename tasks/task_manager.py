from tasks.task import Task
from tasks.database_manager import DatabaseManager
from config import DB_NAME

import ui

from rich.prompt import Prompt

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
                task = ui.create_task()
                self.create_task(task)
            case 2:
                self.update_task(ui.create_task(), self.tasks[Prompt.ask("Select an option", choices=[int(i) for i in range(1, len(self.tasks) + 1)]) - 1])
            case 3:
                self.delete_task()
            case 4:
                sort_by, filter_by = ui.list_options()
                self.list_tasks(self.tasks, sort_by=sort_by, filter_by=filter_by)
            case 5:
                self.exit()

    def create_task(self, task: Task):
        self.tasks.append(task)

    def update_task(self, new_task: Task, old_task: Task):
        for (i, task) in enumerate(self.tasks):
            if task == old_task:
                self.tasks[i] = new_task
                break

    def delete_task(self, task_to_delete: Task):
        pass

    def list_tasks(self, tasks: list[Task], sort_by=None, filter_by=None):
        return Task.compare(tasks, sort_by, filter_by) if sort_by or filter_by else tasks

    def save_to_db(self, tasks: list[Task]):
        pass

    @staticmethod
    def exit():
        raise KeyboardInterrupt
