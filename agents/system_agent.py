# agents/system_agent.py

import os
import subprocess
import webbrowser
from config import APPS

def open_application(app_name: str) -> str:
    app_name = app_name.lower().strip()

    matched_key = None
    for key in APPS:
        if key in app_name or app_name in key:
            matched_key = key
            break

    if not matched_key:
        return f"I don't know how to open {app_name}. You can add it to config.py."

    path = os.path.expandvars(APPS[matched_key])

    try:
        subprocess.Popen(path, shell=True)
        return f"Opening {matched_key} for you."
    except FileNotFoundError:
        return f"Couldn't find {matched_key} at {path}. Please update the path in config.py."
    except Exception as e:
        return f"Couldn't open {matched_key}. Error: {e}"
    
def open_website(url: str) -> str:
    """Opens a URL in Chrome."""
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opening {url} in your browser."

def get_system_info() -> str:
    """Returns basic system info."""
    import psutil, platform
    cpu    = psutil.cpu_percent(interval=1)
    ram    = psutil.virtual_memory()
    used   = round(ram.used  / (1024**3), 1)
    total  = round(ram.total / (1024**3), 1)
    system = platform.system()
    return f"Running {system}. CPU usage is {cpu} percent. RAM usage is {used} of {total} gigabytes."