import csv
# csv module: CSV file read karne ke liye

file_name = "system_metrics.csv"
# wahi CSV file jo Day 2 me bani thi

CPU_THRESHOLD = 70
# rule set kar rahe hain
# CPU 70% se zyada hua to anomaly maanenge

with open(file_name, mode='r') as file:
# CSV file read mode me open ho rahi hai

    reader = csv.DictReader(file)
    # har row ko dictionary ke form me read karega

    for row in reader:
    # CSV ki har line ek-ek karke read hogi

        time = row["Time"]
        # Time column ki value nikal rahe hain

        cpu = float(row["CPU%"])
        # CPU% ko string se number (float) me convert

        if cpu > CPU_THRESHOLD:
        # agar CPU threshold se zyada hai

            print("⚠️ ANOMALY DETECTED | Time:", time, "| CPU:", cpu, "%")
            # warning message print karega

        else:
        # agar CPU normal range me hai

            print("✅ Normal | Time:", time, "| CPU:", cpu, "%")
            # normal status print karega
