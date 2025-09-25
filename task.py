import json
from datetime import datetime

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                self.last_id = data.get("last_id", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
            self.last_id = 0
            self._save_tasks()

    def _save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump({"last_id": self.last_id, "tasks": self.tasks}, f, indent=4)

    def _current_time(self):
        return datetime.utcnow().isoformat()

    def add_task(self, description, status="todo"):
        self.last_id += 1
        new_task = {
            "id": self.last_id,
            "description": description,
            "status": status,
            "createdAt": self._current_time(),
            "updatedAt": self._current_time()
        }
        self.tasks.append(new_task)
        self._save_tasks()
        return new_task

    def update_task(self, task_id, description=None, status=None):
        for task in self.tasks:
            if task["id"] == task_id:
                if description:
                    task["description"] = description
                if status:
                    task["status"] = status
                task["updatedAt"] = self._current_time()
                self._save_tasks()
                return task
        return None  # task not found

    def get_task(self, task_id):
        return next((task for task in self.tasks if task["id"] == task_id), None)

    def get_all_tasks(self):
        return self.tasks

    def delete_task(self, task_id):
        original_len = len(self.tasks)
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        if len(self.tasks) < original_len:
            self._save_tasks()
            return True
        return False

