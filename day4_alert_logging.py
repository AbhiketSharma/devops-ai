import csv
# CSV file read karne ke liye

from datetime import datetime
# current time nikalne ke liye

CSV_FILE = "system_metrics.csv"
# Day 2 wali CSV file

ALERT_FILE = "alerts.log"
# alert log file (new banegi)

CPU_THRESHOLD = 30
# CPU limit, iske upar problem maanenge

with open(CSV_FILE, mode='r') as file:
    # CSV file ko read mode me open kar rahe hain

    reader = csv.DictReader(file)
    # har row dictionary ban jaati hai

    for row in reader:
        # CSV ki har line ko read kar rahe hain

        time = row["Time"]
        # CSV se time value nikaal rahe hain

        cpu = float(row["CPU%"])
        # CPU% ko number me convert kar rahe hain

        if cpu > CPU_THRESHOLD:
            # agar CPU limit cross ho gayi

            alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # alert generate hone ka current time

            alert_message = f"[{alert_time}] CPU ANOMALY | CSV-Time: {time} | CPU: {cpu}%"
            # ek proper alert message bana rahe hain

            print("⚠️ ALERT:", alert_message)
            # terminal me alert dikha rahe hain

            with open(ALERT_FILE, mode='a') as alert_file:
                # alert log file ko append mode me open kar rahe hain

                alert_file.write(alert_message + "\n")
                # alert ko file me likh rahe hain

        else:
            # agar CPU normal hai

            print("✅ Normal | Time:", time, "| CPU:", cpu, "%")
            # normal status sirf print kar rahe hain
