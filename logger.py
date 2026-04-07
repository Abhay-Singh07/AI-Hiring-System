import json
from datetime import datetime
import os


LOG_FILE = "logs.json"


def log_entry(data):
    """
    Append a log entry to logs.json
    """

    entry = {
        "timestamp": datetime.now().isoformat(),
        "data": data
    }

    # Create file if not exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    # Append log
    with open(LOG_FILE, "r+") as f:
        try:
            logs = json.load(f)
        except:
            logs=[]
        logs.append(entry)

        f.seek(0)
        json.dump(logs, f, indent=2)