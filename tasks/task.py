from datetime import datetime
from typing import Union

from config import TIME_FORMAT, CSV_DELIMITER
from tasks.helper import convert_to_datetime, convert_to_bool
from tasks.priority import Priority


class Task:
    def __init__(self, email: str, description: str, complete: bool = False,
                 due_date: datetime = None,
                 priority: Union[Priority, int, str] = Priority("Low"), create_date: datetime = None):
        self.creator_email = email
        self.description = description
        self.complete = convert_to_bool(complete)
        self.due_date = convert_to_datetime(due_date)
        self.priority = priority if isinstance(priority, Priority) else Priority(priority)
        self.create_date = convert_to_datetime(create_date)

    def mark_complete(self):
        self.complete = True

    def pretty_tuple(self):
        return self.description, str(bool(self.complete)), self.due_date.strftime(TIME_FORMAT), str(
            self.priority), self.create_date.strftime(TIME_FORMAT)

    def __str__(self):
        return " - ".join(self.pretty_tuple())

    def __repr__(self):
        return f"Task({','.join(tuple(self))})"

    def __iter__(self):
        return iter((self.creator_email, self.description, int(self.complete), self.due_date.timestamp(),
                     int(self.priority), self.create_date.timestamp()))

    def csv(self):
        values = self.pretty_tuple()
        return f"{CSV_DELIMITER}".join(values)

    def __eq__(self, other):
        return self.description == other.description \
            and self.creator_email == other.creator_email \
            and self.complete == other.complete \
            and self.priority == other.priority
