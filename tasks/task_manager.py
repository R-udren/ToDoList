from datetime import datetime
from operator import attrgetter

from database.database_manager import DatabaseManager
from tasks.task import Task
from tasks.priority import Priority
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
            file.write('description,complete,due_date,priority,create_date\n')
            for task in self.tasks:
                file.write(task.csv() + '\n')
    
    def import_tasks(self, csv_name: str=CSV_NAME):
        with open(csv_name, 'r') as file:
            for line in file:
                if line.startswith('description') and line.endswith('create_date\n'):
                    continue
                _task = line.strip().split(',')
                _task[1] = _task[1] == 'True'
                _task[2] = datetime.strptime(_task[2], TIME_FORMAT).timestamp()
                _task[4] = datetime.strptime(_task[4], TIME_FORMAT).timestamp()
                if not self.task_exists(_task[4]):
                    task = Task(self.email, *_task)
                    self.tasks.append(task)
                    self.db.add_record('tasks', list(task))

    def task_exists(self, task: Task):
        for _task in self.tasks:
            if _task == task:
                return True
        return False
    
    @staticmethod
    def compare(tasks: list, sort_by: str, reversed: bool):
        """
        Compare tasks by sort_by
        :param tasks: list of tasks to compare
        :param sort_by: attribute to sort by (due_date, create_date, priority)
        :param reverse: reverse sort order
        :return: list of tasks
        """
        # Sort tasks
        if sort_by in ["due_date", "create_date", "priority"]:
            tasks.sort(key=attrgetter(sort_by), reverse=reversed)

        return tasks

    @staticmethod
    def search(tasks: list, filter_by: dict):
        """ 
        Compare tasks by filter_by
        :param tasks: list of tasks to compare
        :param filter_by: dictionary of attributes to filter by (complete, priority, due_date, create_date)
        :return: list of tasks
        """
        # Filter tasks
        for key, value in filter_by.items():
            if key == "complete":
                tasks = [task for task in tasks if task.complete == value]
            elif key == "priority":
                value = Priority(value)
                tasks = [task for task in tasks if task.priority == value]
            elif key == "due_date" or key == "create_date":
                value = TaskManager.timestamp(value)
                t1 = value + 86400 * 2
                t2 = value - 86400 * 2
                tasks = [task for task in tasks if t2 < task.due_date < t1]
                return tasks
                
                
        return tasks
    
    @staticmethod
    def timestamp(optionandvalue : str):
        timeamount = optionandvalue.split(" ")
        match timeamount[0]:
            case "Days":
                value = datetime.now().timestamp() + 86400 * int(timeamount[1])
            case "Weeks":
                value = datetime.now().timestamp() + 604800 * int(timeamount[1])
            case "Months":
                value = datetime.now().timestamp() + 2629746 * int(timeamount[1])
            case "Years":
                value = datetime.now().timestamp() + 31556952 * int(timeamount[1])
        return value