import psutil
import time
import os
import subprocess
import json


cpu_threshold = 85
ram_threshold = 85
disk_threshold = 85
ping_response = 100
ping_fail_limit = 3

result = subprocess.run(["ping", "-n", "1", "192.168.10.20"])

memory = psutil.virtual_memory()
disk = psutil.disk_usage('C:')
ip = input("")
ping_info = os.popen(f"ping {ip}").read()

while True:
       print("Logical cores:",
       psutil.cpu_count())
       #How many logical cores do you have
       print("Physical cores:",
       psutil.cpu_count(logical=False))
       #How many physical cores do you have
       print("CPU Usage (%):",
       psutil.cpu_percent(interval=0))
       #While interval of 0 is not ideal because it would return nothing, but due to the time.sleep(1) function this makes it so it updates every 1 sec while in a loop
       print("List of CPU Usage:",
       psutil.cpu_percent(percpu=True))
       print("Total memory (GB):",
       round(memory.total / (1024**3), 2))
       #This is the calculation to make it from bytes to GB
       print ("Used memory (%):",
        memory.percent)
       print("Disk Usage (%):",
       disk.percent)
       print("Free space (GB):",
       round(disk.free / (1024**3), 2))
       time.sleep(1)
       print(ping_info)


# cpu_threshold = 85
# memory_threshold = 85
# disk_threshold = 85


# if memory.percent > memory_threshold:
#     # memory te hoog

# if disk.percent > disk_threshold:
#     # memory te hoog

# if cpu.percent > cpu_threshold:
#     # memory te hoog


""" with open('data.json', '+a') as file:
    values = {'cpu': cpu, 'mem': memory, 'disk': disk}
    json.dump(values, file) """





#Threshold are situational and one thing that I find that was not listed anywhere else except on Reddit was the time. 
#In general the answer is "it depends" but a dimension you are missing here is time. 
# For example, if CPU is above 85% for 10 minutes could be one alarm, and if CPU is above 95% for 30 seconds that could be another alarm. 
# Overall I need to understand usage trends and impacts to app performance and craft rules based on that, rather than seek a cookie cutter set of rules.
#Nonetheless these are the most common threshold I found

#CPU Threshold
# Normal (Idle): Under 10%–15% usage.
# Normal (Under Load): Up to 70%–85% usage.
# Warning / Alert: Sustained usage above 85% to 90% for more than 5 to 10 minutes indicates potential bottlenecks or runaway processes

#RAM (Memory) Threshold
# Normal (Idle): 20%–40% usage depending on total installed capacity.
# Normal (Under Load): Up to 75% usage.
# Warning / Alert: Consistently exceeding 85% to 90% usage risks swapping memory to the storage drive, leading to major system slowdowns.

#Disk Threshold
# Usage Space: Alerts are typically configured when free space drops below 10% to 15% capacity on an OS drive.
#Active Response / Latency (I/O): Average disk response times (latency) exceeding 50 milliseconds (ms) signal severe queue delays or failing mechanical/solid-state drives.

#Ping (Latency) Threshold
# 0–20 ms: Excellent/Ideal (imperceptible delay, optimal for competitive gaming).
# 20–50 ms: Good/Very Good (smooth for streaming, video calls, and general gaming).
# 50–100 ms: Acceptable/Noticeable (fine for casual browsing, but slight delays in fast games).
# 100 ms+: Poor (lag becomes obvious during real-time tasks)



""" computerName = input("What is your computers name? ")
cpuPercentage = int(input("What is your cpu percentage? "))

print("===Server Report===")
print("Computer:", computerName)
print("CPU:", cpuPercentage, "%")

if cpuPercentage <= 50:
    print("Your CPU is cool")
else:
    print("WARNING: CPU TOO HIGH") """