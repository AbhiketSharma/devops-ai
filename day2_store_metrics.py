import psutil
# psutil library: CPU, RAM, Disk ka data lene ke liye

import time
# time module: delay (sleep) dene ke liye

import csv
# csv module: data ko CSV file me likhne ke liye

from datetime import datetime
# datetime: current date & time nikalne ke liye

file_name = "system_metrics.csv"
# CSV file ka naam jisme data store hoga

with open(file_name, mode='a', newline='') as file:
# file open kar rahe hain (append mode = data add hota rahe)

    writer = csv.writer(file)
    # CSV me likhne ke liye writer object

    if file.tell() == 0:
        # agar file bilkul khaali hai (first time run)

        writer.writerow(["Time", "CPU%", "Memory%", "Disk%"])
        # CSV ka header likh rahe hain

while True:
# infinite loop = monitoring continuously chalti rahe

    cpu = psutil.cpu_percent(interval=1)
    # CPU usage percentage (1 second observe karke)

    memory = psutil.virtual_memory().percent
    # RAM ka kitna % use ho raha hai

    disk = psutil.disk_usage('/').percent
    # Root disk (/) ka usage percentage

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # current date & time readable format me

    with open(file_name, mode='a', newline='') as file:
    # dobara file open kar rahe hain data likhne ke liye

        writer = csv.writer(file)
        # writer object dobara create

        writer.writerow([current_time, cpu, memory, disk])
        # ek new row CSV file me add kar rahe hain

    print("Data saved at", current_time)
    # terminal me message dikha raha hai

    time.sleep(5)
    # 5 second rukkar next data collect karega
