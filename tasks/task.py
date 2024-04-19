from datetime import datetime
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

    def __eq__(self, other):
        return self.description == other.description or self.create_date == other.create_date