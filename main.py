import argparse

from ui.main_ui import menu


def main():
    parser = argparse.ArgumentParser(description="To Do List CLI")

    parser.add_argument("--menu", action="store_true", help="Show the menu", default=True)

    parser.add_argument("--email", type=str, help="Email of the user")

    parser.add_argument("--add-task", action="store_true", help="Add a task")
    parser.add_argument("--update-task", action="store_true", help="Update a task")
    parser.add_argument("--delete-task", action="store_true", help="Delete a task")
    parser.add_argument("--mark-complete", action="store_true", help="Mark a task as complete")
    parser.add_argument("--list-tasks", action="store_true", help="List all tasks")
    parser.add_argument("--export-tasks", action="store_true", help="Export tasks to a CSV file")
    parser.add_argument("--import-tasks", action="store_true", help="Import tasks from a CSV file")

    args = parser.parse_args()
    arguments = [args.menu, args.email, args.add_task, args.update_task, args.delete_task, args.mark_complete,
                 args.list_tasks, args.export_tasks, args.import_tasks]
    cli = False
    if any(arguments[1:]):
        arguments[0] = False
        cli = True
    menu(*arguments, cli=cli)


if __name__ == "__main__":
    main()
