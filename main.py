import hashlib
import os
import vt
import time

analyzers = ["https://www.virustotal.com/gui/home/upload", "https://opentip.kaspersky.com/", "https://www.filescan.io/scan", "https://virusscan.jotti.org/", "https://manalyzer.org/"]

users = os.listdir("/home/")
paths = []

for i in users:
    try:
        os.listdir("/home/"+i+"/.vscode")
        paths.append("/home/"+i+"/.vscode/extensions")
    except:
        continue

extensions = {}

for i in paths:
    extensions[i] = os.listdir(i)

for i in extensions.keys():
    extensions[i].pop(extensions[i].index("extensions.json"))
    extensions[i].pop(extensions[i].index(".obsolete"))

for i in extensions.keys():
    for name in extensions[i]:
        os.system(f"zip -r '{name}.zip' '{i+"/"+name}'")

os.system("zip -r all.zip *.zip")

client = vt.Client("my token")
with open("all.zip", "rb") as f:
    analysis = client.scan_file(f, wait_for_completion=True)

with open("reports/vt_report", 'w') as f:
    f.write(str(analysis))

with open("all.zip", "rb") as f:
    hash = hashlib.sha1(f.read()).hexdigest()
file = client.get_object(f"/files/{hash}")

os.system("python vt_parse.py")
print("Всё выполнено")
