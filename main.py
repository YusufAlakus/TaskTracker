#!/usr/bin/env python3
import sys
from task import TaskManager

def print_task(task):
    print(f"[{task['id']}] {task['description']} ({task['status']}) - Created: {task['createdAt']}, Updated: {task['updatedAt']}")

def main():
    manager = TaskManager()

    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return

    command = sys.argv[1]

    try:
        if command == "add":
            description = " ".join(sys.argv[2:])
            task = manager.add_task(description)
            print(f"Task added successfully (ID: {task['id']})")

        elif command == "update":
            task_id = int(sys.argv[2])
            description = " ".join(sys.argv[3:])
            task = manager.update_task(task_id, description=description)
            if task:
                print(f"Task {task_id} updated successfully")
            else:
                print(f"Task {task_id} not found")

        elif command == "delete":
            task_id = int(sys.argv[2])
            if manager.delete_task(task_id):
                print(f"Task {task_id} deleted successfully")
            else:
                print(f"Task {task_id} not found")

        elif command == "mark-in-progress":
            task_id = int(sys.argv[2])
            task = manager.update_task(task_id, status="in-progress")
            if task:
                print(f"Task {task_id} marked as in-progress")
            else:
                print(f"Task {task_id} not found")

        elif command == "mark-done":
            task_id = int(sys.argv[2])
            task = manager.update_task(task_id, status="done")
            if task:
                print(f"Task {task_id} marked as done")
            else:
                print(f"Task {task_id} not found")

        elif command == "list":
            status_filter = sys.argv[2] if len(sys.argv) > 2 else None
            tasks = manager.get_all_tasks()
            if status_filter:
                tasks = [t for t in tasks if t["status"] == status_filter]
            if not tasks:
                print("No tasks found")
            for task in tasks:
                print_task(task)

        else:
            print("Unknown command:", command)

    except IndexError:
        print("Error: Missing arguments for command")
    except ValueError:
        print("Error: Task ID must be a number")

if __name__ == "__main__":
    main()
