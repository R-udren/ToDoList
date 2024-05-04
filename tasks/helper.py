from datetime import datetime

from config import TIME_FORMAT


def convert_to_datetime(date, default=None):
    if date is None:
        return default or datetime.now()
    elif isinstance(date, datetime):
        return date
    elif isinstance(date, float):
        return datetime.fromtimestamp(date)
    elif isinstance(date, str):
        return datetime.strptime(date, TIME_FORMAT)
    else:
        raise ValueError("Invalid date")


def convert_to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ["true", "1"]
    if isinstance(value, int):
        return bool(value)
    raise ValueError("Invalid boolean value")
