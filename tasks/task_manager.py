from datetime import datetime
from operator import attrgetter

from config import DB_NAME, CSV_NAME
from database.csv_manager import CSVManager
from database.database_manager import DatabaseManager
from tasks.priority import Priority
from tasks.task import Task


class TaskManager:
    commandsV = [
        "Exit",
        "Manage tasks",
        "List all tasks",
        "Export to CSV",
        "Import from CSV"
    ]

    commandsM = [
        "Exit",
        "Create a task",
        "Update a task",
        "Delete a task",
        "Mark task as complete"
    ]

    def __init__(self, email: str):
        self.db = DatabaseManager(DB_NAME)
        self.db.create_task_table("tasks", ["email TEXT", "description TEXT", "complete INTEGER", "due_date REAL",
                                            "priority INTEGER", "create_date REAL"])
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

    def mark_complete(self, task: Task):
        for (i, _task) in enumerate(self.tasks):
            if _task == task:
                self.tasks[i].complete = True
                self.db.clear_table('tasks', self.email)
                self.save_to_db()
                break

    def delete_task(self, task_to_delete: Task):
        self.tasks.remove(task_to_delete)
        self.db.clear_table('tasks', self.email)
        self.save_to_db()

    def save_to_db(self):
        for task in self.tasks:
            self.db.add_record('tasks', list(task))

    def export_tasks(self, csv_name: str = CSV_NAME):
        header = "description,complete,due_date,priority,create_date"
        data = [task.csv() for task in self.tasks]
        written_rows = CSVManager.export_csv(data, header, csv_name)
        return written_rows

    def import_tasks(self, path: str = CSV_NAME):
        header = "description,complete,due_date,priority,create_date"
        data = CSVManager.import_csv(header, path)
        counter = 0
        for row in data:
            if not self.task_exists(Task(*row)):
                self.tasks.append(Task(*row))
                self.db.add_record('tasks', row)
                counter += 1
        return counter

    def task_exists(self, task: Task):
        for _task in self.tasks:
            if _task == task:
                return True
        return False

    @staticmethod
    def compare(tasks: list, sort_by: str, reverse: bool):
        """
        Compare tasks by sort_by
        :param tasks: list of tasks to compare
        :param sort_by: attribute to sort by (due_date, create_date, priority)
        :param reverse: reverse sort order
        :return: list of tasks
        """
        # Sort tasks
        if sort_by in ["due_date", "create_date", "priority"]:
            tasks.sort(key=attrgetter(sort_by), reverse=reverse)

        return tasks

    @staticmethod
    def filter_tasks(tasks: list, filter_by: dict):
        """ 
        Compare tasks by filter_by
        :param tasks: list of tasks to compare
        :param filter_by: dictionary of attributes to filter by (complete, priority, due_date, create_date)
        """
        matching_tasks = found_tasks = []
        for option, value in filter_by.items():
            option = option.capitalize()
            if option == "Complete":
                found_tasks = [task for task in tasks if task.complete == value]
            elif option == "Priority":
                value = Priority(value)
                found_tasks = [task for task in tasks if task.priority == value]
            elif option == "Due date" or option == "Create date":
                value = TaskManager.time_stamp_value(value)
                t1 = value - 86400 * 2
                t2 = value + 86400 * 2
                found_tasks = [task for task in tasks if t1 < task.due_date.timestamp() < t2]
            matching_tasks = [task for task in found_tasks if task in tasks]
            tasks = matching_tasks

        return matching_tasks

    @staticmethod
    def time_stamp_value(option_and_value: str):
        time_amount = option_and_value.split(" ")
        value = datetime.now().timestamp()
        match time_amount[0]:
            case "Days":
                value += 86400 * int(time_amount[1])
            case "Weeks":
                value += 604800 * int(time_amount[1])
            case "Months":
                value += 2629746 * int(time_amount[1])
            case "Years":
                value += 31556952 * int(time_amount[1])
        return value
