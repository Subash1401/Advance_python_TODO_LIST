import csv
import json
import shutil
from pathlib import Path

# file and folder path design panadra

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
BACKUP_DIR = DATA_DIR / "backup"
EXPORT_DIR = BASE_DIR / "exports"

TASKS_FILE = DATA_DIR / "tasks.json"
BACKUP_FILE = BACKUP_DIR / "tasks_backup.json"


# App Data
tasks = []
next_task_id = 1

# create folders
def setup_folders():

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)


# save panna data check(validate)

def validate_tasks(data):

    if not isinstance(data, list):
        raise ValueError("Tasks data must be a list.")

    seen_ids = set()

    for task in data:
        if not isinstance(task, dict):
            raise ValueError("Each task must be a dictionary.")

        required_keys = {
            "id",
            "title",
            "description",
            "completed",
            "created_at"
        }

        if not required_keys.issubset(task.keys()):
            raise ValueError("A task is missing required fields.")

        task_id = task["id"]

        if type(task_id) is not int or task_id <= 0:
            raise ValueError("Invalid task ID.")

        if task_id in seen_ids:
            raise ValueError("Duplicate task ID.")

        if not isinstance(task["title"], str):
            raise ValueError("Invalid task title.")

        if not isinstance(task["description"], str):
            raise ValueError("Invalid task description.")

        if type(task["completed"]) is not bool:
            raise ValueError("Invalid completion status.")

        if not isinstance(task["created_at"], str):
            raise ValueError("Invalid creation date.")

        seen_ids.add(task_id)

    return data

# read and validate the json file

def read_tasks_file(file_path):

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return validate_tasks(data)



# Automatic ah backup edukum 

def create_backup():

    if not TASKS_FILE.exists():
        return

    try:
        read_tasks_file(TASKS_FILE)
        shutil.copy2(TASKS_FILE, BACKUP_FILE)

    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Backup warning: {error}")


# task ah permanent ah save pandra

def save_tasks():

    temporary_file = DATA_DIR / "tasks.tmp" 

    try:
        create_backup()

        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(
                tasks,
                file,
                indent=4,
                ensure_ascii=False
            )

        temporary_file.replace(TASKS_FILE)

        print("Data saved successfully.")

    except (OSError, TypeError, ValueError) as error:
        print(f"Save failed: {error}")
        print("Your latest changes may not be saved.")

        if temporary_file.exists():
            try:
                temporary_file.unlink()
            except OSError:
                pass


# restore tasks from backup 

def restore_backup():

    global tasks, next_task_id

    try:
        restored_tasks = read_tasks_file(BACKUP_FILE)

        tasks = restored_tasks
        next_task_id = max(
            (task["id"] for task in tasks),
            default=0
        ) + 1

        print("Tasks restored from backup.")
        return True

    except FileNotFoundError:
        print("No backup file found.")
        return False

    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Backup not restored : {error}")
        return False



#load pannum task previous use panna task ellam (program start pandra apo)

def load_tasks():

    global tasks, next_task_id

    try:
        loaded_tasks = read_tasks_file(TASKS_FILE)

        tasks = loaded_tasks

        next_task_id = max(
            (task["id"] for task in tasks),
            default=0
        ) + 1

        print(f"Loaded {len(tasks)} task(s).")

    except FileNotFoundError:
        tasks = []
        next_task_id = 1

        print("No saved tasks . Starting fresh.")

    except json.JSONDecodeError as error:
        print(f"Tasks file contains invalid JSON: {error}")

        if not restore_backup():
            tasks = []
            next_task_id = 1
            print("Starting with an empty task list.")

    except (OSError, ValueError) as error:
        print(f"Could not load tasks: {error}")

        if not restore_backup():
            tasks = []
            next_task_id = 1
            print("Starting with an empty task list.")




# input validation check pandra

def get_non_empty_input(message):

    while True:
        value = input(message).strip()

        if value: 
            return value

        print("Input cannot be empty, Pls retry")


def get_task_id():
    while True:
        try: 
            task_id=int(input("Enter task id: "))

            if task_id > 0:
                return task_id

            print("Task id must be greater than Zero")

        except ValueError:
            print("please enter valid number")


def find_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return None