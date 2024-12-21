import os
import requests

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

url = "https://opentip.kaspersky.com/ui/uploadsample"

headers = {
    "Host": "opentip.kaspersky.com",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryDybPIAiTWEuWPbWb",
    "Accept-Encoding": "gzip, deflate, br",
}

files = {
    'file': ('all.zip', open("all.zip", 'rb'), 'application/zip'),
}

data = {
    'name': 'ext.zip',
    'silent': 'false',
    'fullReportNeeded': 'true'
}

response = requests.post(url, headers=headers, files=files, data=data, verify=False)
print(response)
