from datetime import datetime
from tasks.priority import Priority


class Task:
    def __init__(self, description: str, status: bool = False, due_date: str = None, priority: Priority = Priority("Low")):
        self.description = description
        self.complete = status
        self.due_date = due_date
        self.priority = priority
