import csv
import time
from datetime import datetime

# =========================
# FILES
# =========================
CSV_FILE = "system_metrics.csv"
ALERT_FILE = "alerts.log"
HEALING_FILE = "healing.log"
STATE_FILE = "state.txt"
COOLDOWN_FILE = "cooldown.txt"

# =========================
# SETTINGS
# =========================
CPU_THRESHOLD = 40        # demo ke liye
CHECK_INTERVAL = 10       # seconds
COOLDOWN_SECONDS = 60     # 1 minute cooldown

# =========================
# AUTO-HEALING FUNCTION
# =========================
def auto_heal(cpu_value, csv_time):
    heal_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    heal_message = (
        f"[{heal_time}] AUTO-HEALING | "
        f"High CPU ({cpu_value}%) | CSV-Time: {csv_time} | "
        f"Action: Restart service (SIMULATED)"
    )

    print("🔧", heal_message)

    with open(HEALING_FILE, "a") as f:
        f.write(heal_message + "\n")

    # cooldown start time save
    with open(COOLDOWN_FILE, "w") as f:
        f.write(str(time.time()))

# =========================
# READ LAST STATE
# =========================
def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# =========================
# MAIN LOOP (REAL-TIME)
# =========================
print("🚀 Real-time AIOps monitoring started (CTRL+C to stop)")

while True:
    last_time = read_file(STATE_FILE)
    last_cooldown = read_file(COOLDOWN_FILE)

    # CSV read
    rows = []
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)

    if not rows:
        print("No data in CSV")
        time.sleep(CHECK_INTERVAL)
        continue

    latest = rows[-1]
    csv_time = latest["Time"]
    cpu = float(latest["CPU%"])

    # duplicate check
    if csv_time == last_time:
        print("ℹ️ No new data. Waiting...")
        time.sleep(CHECK_INTERVAL)
        continue

    # cooldown check
    if last_cooldown:
        diff = time.time() - float(last_cooldown)
        if diff < COOLDOWN_SECONDS:
            print("⏳ Cooldown active. Skipping healing.")
            with open(STATE_FILE, "w") as f:
                f.write(csv_time)
            time.sleep(CHECK_INTERVAL)
            continue

    # decision
    if cpu > CPU_THRESHOLD:
        alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        alert_message = (
            f"[{alert_time}] CPU ANOMALY | "
            f"CSV-Time: {csv_time} | CPU: {cpu}%"
        )

        print("⚠️ ALERT:", alert_message)

        with open(ALERT_FILE, "a") as f:
            f.write(alert_message + "\n")

        auto_heal(cpu, csv_time)

    else:
        print("✅ Normal | Time:", csv_time, "| CPU:", cpu, "%")

    # save processed state
    with open(STATE_FILE, "w") as f:
        f.write(csv_time)

    time.sleep(CHECK_INTERVAL)
