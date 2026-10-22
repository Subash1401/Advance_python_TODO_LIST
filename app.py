from datetime import datetime
import Advance_python_TODO_LIST.val as v


# task Add

def add_task():
    global next_task_id

    print ("\n---- Add New Task -----")

    title = v.get_non_empty_input("Title title: ")
    description = input("Description (optional):  ").strip()

    task = {
        "id": v.next_task_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at":datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    v.tasks.append(task)
    v.next_task_id += 1

    v.save_tasks()

    print(f"\nTask added sucessfully! ID: {task['id']}")



# View all tasks

def view_tasks():
    print("\n----- All tasks -------")

    if not v.tasks:
        print("No task found , Add your first task")
        return

    for task in v.tasks:
        status="COMPLETED" if task["completed"] else "PENDING"

        print("_"*50)
        print(f"ID           : {task['id']}")
        print(f"Title        : {task['title']}")
        print(f"Description  : {task['description'] or 'None'}")
        print(f"Completed    : {status}")
        print(f"Created at   : {task['created_at']}")
    print("_"*50)



# Complete task

def complete_task():
    print("\n----- Complete task -------")

    task_id=v.get_task_id()
    task=v.find_task(task_id)

    if task is None:
        print("task is not found")
        return

    if task["completed"]:
        print("This task is already completed")
        return

    task["completed"] = True

    v.save_tasks()

    print(f"task {task['title']} completed successfully")



# update task

def update_task():
    print("\n----- Update task -------")

    task_id=v.get_task_id()
    task=v.find_task(task_id)

    if task is None:
        print("task not found ")
        return

    print("Press enter to keep the existing value")

    new_title=input(f"New title [{task['title']}]: ").strip()

    new_description=input(f"New description [{task['description']}]: ").strip()

    if new_title:
        task["title"] = new_title

    if new_description:
        task["description"] = new_description

    v.save_tasks()

    print("Task updated successfully!")



# delete task

def delete_task():
    print("\n----- delete task -------")

    task_id=v.get_task_id()
    task=v.find_task(task_id)

    if task is None:
        print("task not found ")
        return

    conformation = input(f"Delete '{task['title']}'? (yes/no)").strip().lower()

    if conformation=='yes':
        v.tasks.remove(task)

        v.save_tasks()

        print("task deleted successfully")
    else:
        print("delete cancelled")


# search task

def search_task():
    print("\n----- search task -------")

    keyword = v.get_non_empty_input("Enter the title or description keyword: ").casefold()

    matches = [
        task for task in v.tasks
        if keyword in task["title"].casefold()  
        or keyword in task["description"].casefold()
    ]

    if not matches:
        print("NO matching tasks found")
        return

    for task in matches:
        status = "COMPLETED" if task["completed"] else "PENDING"

        print(
            f"ID : {task['id']} |"
            f"Title : {task['title']} |"
            f"Status : {status} "

        )


# product summary

def show_summary():

    total = len(v.tasks)
    completed = sum(task["completed"] for task in v.tasks)

    pending = total - completed

    percentage = (
        completed / total * 100
        if total > 0
        else 0
    )

    print("\n--- PRODUCTIVITY SUMMARY ---")
    print(f"Total tasks     : {total}")
    print(f"Completed tasks : {completed}")
    print(f"Pending tasks   : {pending}")
    print(f"Completion rate : {percentage:.1f}%")


# TXT

def export_txt():
    try:
        with (v.EXPORT_DIR / "tasks_report.txt").open(
            "w", encoding="utf-8"
        ) as file:

            file.write("SMART TODO LIST PRO REPORT\n")
            file.write("=" * 40 + "\n\n")

            for task in v.tasks:
                status = "COMPLETED" if task["completed"] else "PENDING" 

                file.write(f"ID: {task['id']}\n")
                file.write(f"Title: {task['title']}\n")
                file.write(f"Description: {task['description']}\n")
                file.write(f"Status: {status}\n")
                file.write(f"Created: {task['created_at']}\n")
                file.write("-" * 30 + "\n")

        print("TXT report exported successfully.")

    except OSError as error:
        print(f"TXT export failed: {error}")


# CSV

def export_csv():
    fields = [
        "id",
        "title",
        "description",
        "completed",
        "created_at"
    ]

    try:
        with (v.EXPORT_DIR / "tasks_report.csv").open(
            "w", newline="", encoding="utf-8"
        ) as file:

            writer = v.csv.DictWriter(
                file,
                fieldnames=fields,
                extrasaction="ignore"
            )

            writer.writeheader()
            writer.writerows(v.tasks)

        print("CSV report exported successfully.")

    except OSError as error:
        print(f"CSV export failed: {error}")


# Manual option kuduthu restore pandro

def manual_restore():
    confirmation = input(
        "Restore tasks from backup? "
        "Current in-memory tasks will be replaced. (yes/no): "
    ).strip().lower()

    if confirmation == "no":
        print("Restore cancelled.")
        return

    if v.restore_backup():

        v.save_tasks()




# main menu

def show_menu():
    print("\n" + "="*50)
    print("       SMART TODO LIST    ")
    print("="*50)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Complete Task")
    print("4. Update Task")
    print("5. Delete Task")
    print("6. Search Tasks")
    print("7. Productivity Summary")
    print("8. Export TXT File")
    print("9. ExpORt CSV File")
    print("10. Manual Restore")
    print("0.  Exist")
    print("=" * 50)



def main ():
    v.setup_folders()
    v.load_tasks()

    print("Welcome to subash smart todo list")

    while True:
        show_menu()
        choice = int(input("Choose an option :  "))

        try :
            match choice:
                case 1:
                    add_task()
                case 2:
                    view_tasks()
                case 3:
                    complete_task()
                case 4:
                    update_task()
                case 5: 
                    delete_task()
                case 6:
                    search_task()
                case 7:
                    show_summary()
                case 8: 
                    export_txt()
                case 9:
                    export_csv()
                case 10:
                    manual_restore()
                case 0:
                    print("Byeee Byeeee!!!!")
                    break
                case _:
                    print("INvalid choice enter again!")

        except (EOFError, KeyboardInterrupt):
            print("\nApplication closed.")
            break


if __name__ == "__main__":
    main()




    
