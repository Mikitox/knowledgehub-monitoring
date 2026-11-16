import psutil
import json
import requests
import socket

cpu_threshold = 10
memory_threshold = 10
disk_threshold = 10

memory = psutil.virtual_memory()
disk = psutil.disk_usage('C:')
cpu = psutil.cpu_percent(interval=0)

cpu_alert=False
mem_alert=False
disk_alert=False
if memory.percent > memory_threshold:
    mem_alert=True

if disk.percent > disk_threshold:
    disk_alert=True

if cpu > cpu_threshold:
    cpu_alert=True

values = {
    'cpu': cpu,
    'mem': memory.percent,
    'disk': disk.percent,
    'cpu_alert': cpu_alert
}

values["hostname"] = socket.gethostname()

print("Sending data...")
print(values)

try:

     response = requests.post(
          "http://192.168.10.20:5000/metrics",
          json=values,
          timeout=5
     )

     print("Status:", response.status_code)
     print(response.text)

except Exception as e:

     print("ERROR:", e)


with open('data.json', '+a') as file:
    values = {'cpu': cpu, 'mem': memory.percent, 'disk': disk.percent, "cpu_alert": cpu_alert}
    json.dump(values, file)


with open('incidents.json', '+a') as file:
        file.write("DISK HIGH")