from datetime import datetime
from operator import attrgetter


from tasks.priority import Priority
from config import TIME_FORMAT


class Task:
    def __init__(self, user_id : str, description: str, complete: bool = False,
                 due_date: str = None, priority: Priority = Priority("Low"), create_date: str = None):
        self.creator_id = user_id
        self.description = description
        self.complete = complete
        self.due_date = due_date
        self.priority = Priority(priority).level
        self.create_date = create_date if create_date is not None else datetime.now().strftime(TIME_FORMAT)

    @staticmethod
    def compare(tasks: list, sort_by: str, filter_by: dict, reverse: bool = False):
        """
        Compare tasks by sort_by and filter_by
        :param tasks: list of tasks to compare
        :param sort_by: attribute to sort by (due_date, create_date, priority)
        :param filter_by: dictionary of attributes to filter by (complete, priority, due_date, create_date)
        :param reverse: reverse sort order
        :return: list of tasks
        """
        # Filter tasks
        for key, value in filter_by.items():
            if key == "complete":
                tasks = [task for task in tasks if task.complete == value]
            elif key == "priority":
                tasks = [task for task in tasks if task.priority == value]
            elif key == "due_date":
                tasks = [task for task in tasks if task.due_date == value]
            elif key == "create_date":
                tasks = [task for task in tasks if task.create_date == value]

        # Sort tasks
        if sort_by in ["due_date", "create_date", "priority"]:
            tasks.sort(key=attrgetter(sort_by), reverse=reverse)

        return tasks


