import csv
from datetime import datetime

# =========================
# FILE NAMES
# =========================
CSV_FILE = "system_metrics.csv"
ALERT_FILE = "alerts.log"
HEALING_FILE = "healing.log"

# =========================
# THRESHOLD
# =========================
CPU_THRESHOLD = 40   # demo ke liye low rakha hai

# =========================
# AUTO-HEALING FUNCTION
# =========================
def auto_heal(cpu_value, csv_time):
    heal_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    heal_message = (
        f"[{heal_time}] AUTO-HEALING TRIGGERED | "
        f"Reason: High CPU ({cpu_value}%) | "
        f"CSV-Time: {csv_time} | "
        f"Action: Restarting service (SIMULATED)"
    )

    print("🔧", heal_message)

    with open(HEALING_FILE, mode='a') as heal_file:
        heal_file.write(heal_message + "\n")

# =========================
# MAIN LOGIC
# =========================
with open(CSV_FILE, mode='r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        time = row["Time"]
        cpu = float(row["CPU%"])

        if cpu > CPU_THRESHOLD:
            alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            alert_message = (
                f"[{alert_time}] CPU ANOMALY | "
                f"CSV-Time: {time} | CPU: {cpu}%"
            )

            print("⚠️ ALERT:", alert_message)

            with open(ALERT_FILE, mode='a') as alert_file:
                alert_file.write(alert_message + "\n")

            # AUTO-HEALING CALL
            auto_heal(cpu, time)

        else:
            print("✅ Normal | Time:", time, "| CPU:", cpu, "%")
