from datetime import datetime
from operator import attrgetter
from typing import Union


from tasks.priority import Priority
from config import TIME_FORMAT


class Task:
    def __init__(self, email : str, description: str, complete: bool = False,
                 due_date: datetime.timestamp = None, priority: Union[Priority, int, str] = Priority("Low"), create_date: int = None):
        self.creator_email = email
        self.description = description
        self.complete = bool(complete)
        self.due_date = due_date if due_date is not None else datetime.now().timestamp()
        if isinstance(priority, Priority):
            self.priority = priority
        else:
            self.priority = Priority(priority)
        self.create_date = create_date if create_date is not None else datetime.now().timestamp()

    def mark_complete(self):
        self.complete = True

    def pretty_tuple(self):
        return self.description, str(bool(self.complete)), datetime.fromtimestamp(self.due_date).strftime(TIME_FORMAT), str(self.priority), datetime.fromtimestamp(self.create_date).strftime(TIME_FORMAT)

    def __str__(self):
        return " - ".join(self.pretty_tuple())

    def __iter__(self):
        return iter((self.creator_email, self.description, int(self.complete), self.due_date, int(self.priority), self.create_date))

    def csv(self):
        return ','.join(self.pretty_tuple())

    @staticmethod
    def compare(tasks: list, sort_by: str, reversed : bool):
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
            elif key == "due_date":
                
                value = Task.timestamp(value)
                t1 = value + 86400 * 2
                t2 = value - 86400 * 2
                tasks = [task for task in tasks if t2 < task.due_date < t1]
                return tasks
            elif key == "create_date":
                value = Task.timestamp(value)
                t1 = value + 86400 * 2
                t2 = value - 86400 * 2
                tasks = [task for task in tasks if t2 < task.due_date < t1]
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


