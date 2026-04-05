import datetime
import inspect

def log(message, source="Server", level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get the calling function name
    caller = inspect.stack()[1].function
    
    print(f"[{timestamp}] [{level}] [{caller}] [{source}] {message}")