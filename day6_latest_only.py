import csv
from datetime import datetime

# =========================
# FILES
# =========================
CSV_FILE = "system_metrics.csv"
ALERT_FILE = "alerts.log"
HEALING_FILE = "healing.log"
STATE_FILE = "state.txt"   # last processed time store karega

# =========================
# THRESHOLD
# =========================
CPU_THRESHOLD = 40   # demo ke liye low

# =========================
# AUTO-HEALING
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

# =========================
# LAST PROCESSED TIME
# =========================
last_time = None
try:
    with open(STATE_FILE, "r") as f:
        last_time = f.read().strip()
except FileNotFoundError:
    last_time = None

# =========================
# READ CSV (LATEST ROW)
# =========================
rows = []
with open(CSV_FILE, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        rows.append(row)

if not rows:
    print("No data in CSV")
    exit()

latest = rows[-1]
csv_time = latest["Time"]
cpu = float(latest["CPU%"])

# =========================
# DUPLICATE CHECK
# =========================
if csv_time == last_time:
    print("ℹ️ Already processed this entry. No action.")
    exit()

# =========================
# DECISION
# =========================
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

# =========================
# SAVE STATE
# =========================
with open(STATE_FILE, "w") as f:
    f.write(csv_time)
