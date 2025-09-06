import time
from datetime import datetime
import pyttsx3
import json
import os

TASKS_FILE = "tasks.json"
engine = pyttsx3.init()

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def reminder_loop():
    """Continuously check tasks and notify when due"""
    while True:
        now = datetime.now().replace(second=0, microsecond=0)
        tasks = load_tasks()
        updated_tasks = []

        for task in tasks:
            if task.get("time") == str(now):
                message = f"Reminder: {task['task']}"
                print(f"🔔 {message}")
                engine.say(message)
                engine.runAndWait()
                # Do NOT re-add to updated_tasks → removes it after reminding
            else:
                updated_tasks.append(task)

        # Save back updated list
        save_tasks(updated_tasks)

        time.sleep(60)  # check every minute
