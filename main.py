from task_manager import add_task, get_voice_input, load_tasks
from reminder import reminder_loop
import threading

if __name__ == "__main__":
    print("📌 AI To-Do List with Reminders")
    print("Type your task (e.g., 'Remind me to call mom at 9 pm')")
    print("Or type 'voice' to speak the task")
    print("Type 'exit' to quit\n")

    # Load existing tasks
    tasks = load_tasks()

    # Run reminder loop in a separate thread
    reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
    reminder_thread.start()

    while True:
        user_input = input("👉 Enter task (or 'voice' / 'exit'): ")

        if user_input.lower() == "exit":
            print("👋 Exiting...")
            break
        elif user_input.lower() == "voice":
            text = get_voice_input()
            if text:
                add_task(text)
        else:
            add_task(user_input)
