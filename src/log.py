from path import LOG_FILE
import time

# Basic timestamp function
def timestamp():
    return time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())

# Basic logging function
def log(error):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp()}]: {str(error)}\n")