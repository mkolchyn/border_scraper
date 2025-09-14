import os
from dotenv import load_dotenv
import threading
import time
import subprocess
from datetime import datetime

# Get intervals from environment
VISUALIZER_INTERVAL = int(os.getenv("VISUALIZER_INTERVAL", 300))  # default 5 min
VISUALIZER_STATS_INTERVAL = int(os.getenv("VISUALIZER_STATS_INTERVAL", 600))  # default 10 min

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_file(script_name):
    return os.path.join(LOG_DIR, f"{script_name}.log")

def run_script(script_name, interval):
    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Running {script_name}")
            with open(log_file(script_name), "a") as f:
                subprocess.run(["python", f"{script_name}.py"], check=True, stdout=f, stderr=f)
        except Exception as e:
            with open(log_file(script_name), "a") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error: {e}\n")
        time.sleep(interval)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_script, args=("visualizer_stats", VISUALIZER_STATS_INTERVAL), daemon=True)
    t2 = threading.Thread(target=run_script, args=("visualizer", VISUALIZER_INTERVAL), daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
