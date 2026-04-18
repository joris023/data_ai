import datetime
import inspect

def log(message, level="INFO"):
    return
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    caller = inspect.stack()[1].function

    print(f"[{timestamp}] [{level}] [{caller}] {message}")