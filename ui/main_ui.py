
from typing import Union

from rich.console import Console
from rich.table import Table


from users.user import User
from tasks.task import Task



console = Console()


def create_table(name : str, commands : list[Union[str, Task, User]]):
    table = Table(title=name.capitalize, title_style="bold blue")
    table.add_column("Nr", style="cyan", justify="center")
    if isinstance(commands[0], Task):
        table.add_column("Description", style="magenta")
        table.add_column("Complete", style="green")
        table.add_column("Due Date", style="yellow")
        table.add_column("Priority", style="red")
        table.add_column("Create Date", style="blue")

        for i, option in enumerate(commands, 1):
            table.add_row(str(i), *option.pretty_tuple())
        return table

    elif isinstance(commands[0], User):
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="magenta")

        for i, option in enumerate(commands, 1):
            table.add_row(str(i), option.email, option.username)
        return table
    else:
        table.add_column("Description", style="magenta")

        for i, option in enumerate(commands, 1):
            table.add_row(str(i), option)
        return table