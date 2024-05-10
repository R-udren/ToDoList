# To Do List

Console Task management app written on Python. Supports adding, removing, listing, marking tasks as done, exporting and
importing tasks from a file.

## Features

- Add tasks
- Remove tasks
- List tasks
- Mark tasks as done
- Export tasks to a file
- Import tasks from a file

## Requirements

- Python 3.6 or higher
- Required packages are listed in `requirements.txt`
- OS that supports Python

## Installation

1. Clone the repository

   ```bash
   git clone https://github.com/R-udren/ToDoList
   ```

   ```bash
   cd ToDoList
   ```

2. Install the dependencies
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Run the app
   ```bash
   python main.py
   ```

## Usage

Uses a CLI to interact with the app.

Ctrl + C several times to exit the app.

The app can be run in two ways: classic usage and CLI.

### Classic usage

```bash
python main.py
```

### CLI

List all possible commands

```bash
main.py --help
```

Example of adding a task

```bash
python main.py --email example@mail.com --add-task
```
