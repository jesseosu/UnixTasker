import time
import subprocess
import logging

logging.basicConfig(filename='task_scheduler.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_event(message):
    logging.info(message)

def read_schedule(file_path):
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        schedule = []
        for line in lines:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split(None, 5)
            if len(parts) != 6:
                continue
            minute, hour, day, month, weekday, command = parts
            schedule.append((minute, hour, day, month, weekday, command))
        return schedule
    except Exception as e:
        log_event(f"Error reading schedule from {file_path}: {e}")
        return []

def match(field, current):
    return field == "*" or field == str(current)

def check_and_run(schedule):
    now = time.localtime()
    for minute, hour, day, month, weekday, command in schedule:
        if (match(minute, now.tm_min) and match(hour, now.tm_hour) and
            match(day, now.tm_mday) and match(month, now.tm_mon) and
            match(weekday, now.tm_wday)):
            log_event(f"Executing: {command}")
            try:
                subprocess.Popen(command, shell=True)
                log_event(f"Successfully executed: {command}")
            except Exception as e:
                log_event(f"Error executing {command}: {e}")

def main():
    schedule = read_schedule("schedule.txt")
    if not schedule:
        log_event("No tasks to schedule.")
        print("No tasks to schedule.")
        return

    print("🕒 Mini Task Scheduler Started 🕒")
    try:
        while True:
            check_and_run(schedule)
            time.sleep(60)
    except KeyboardInterrupt:
        log_event("Scheduler stopped by user.")
        print("Scheduler stopped.")

if __name__ == "__main__":
    main()
