import re
import dateparser
import json
import os
import speech_recognition as sr

TASKS_FILE = "tasks.json"

# ---------------------- CLEAN TASK ----------------------
def clean_task(text):
    """
    Remove common time/date phrases from the text using regex.
    Example: "Remind me to call mom at 9 pm" -> "call mom"
    """
    text = text.lower().strip()

    # Remove leading "remind me to"
    text = re.sub(r"^remind me to", "", text).strip()

    # Remove trailing time/date words like "at 9 pm", "tomorrow", "tonight"
    text = re.sub(r"\b(at|on|by|tomorrow|today|tonight|next|am|pm)\b.*", "", text).strip()

    return text

# ---------------------- PARSE TASK ----------------------
def parse_task(text):
    """Extract structured task with time"""
    # First try parsing the full sentence
    time = dateparser.parse(
        text,
        settings={"PREFER_DATES_FROM": "future", "RETURN_AS_TIMEZONE_AWARE": False}
    )

    task = clean_task(text)

    # If failed, try parsing only the part after "at" (e.g. "9 pm")
    if not time:
        match = re.search(r"\b(at|by|on)\s+(.*)", text)
        if match:
            time = dateparser.parse(
                match.group(2),
                settings={"PREFER_DATES_FROM": "future", "RETURN_AS_TIMEZONE_AWARE": False}
            )

    return {"task": task, "time": time.strftime("%Y-%m-%d %H:%M:%S") if time else None}



# ---------------------- SAVE TASK ----------------------
def add_task(text):
    """Parse, add, and save task to file"""
    task_data = parse_task(text)
    tasks = load_tasks()
    tasks.append(task_data)

    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

    print(f"✅ Task added: {task_data['task']} at {task_data['time']}")

# ---------------------- LOAD TASKS ----------------------
def load_tasks():
    """Load all tasks from file"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

# ---------------------- VOICE INPUT ----------------------
def get_voice_input():
    """Take voice input and convert to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Say your task...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("🗣️ You said:", text)
        return text
    except:
        print("❌ Could not understand voice input")
        return None
