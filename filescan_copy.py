import os
import subprocess

users = os.listdir("/home/")
paths = []

for i in users:
    try:
        os.listdir("/home/"+i+"/.vscode")
        paths.append("/home/"+i+"/.vscode/extensions")
    except:
        continue

print(paths)

extensions = {}

for i in paths:
    extensions[i] = os.listdir(i)

for i in extensions.keys():
    extensions[i].pop(extensions[i].index("extensions.json"))
    extensions[i].pop(extensions[i].index(".obsolete"))

print(extensions) 


temp_dir = subprocess.check_output(["mktemp", "-d"]).decode().strip()
print(temp_dir)

for path_to_ext in extensions.keys():
    name = path_to_ext.split('/')[2]
    os.system(f"mkdir {temp_dir}/{name}")
    for sub_ext in extensions[path_to_ext]:
        ext = path_to_ext + "/" + sub_ext
        print(ext)
        os.system(f"mkdir {temp_dir}/{name}/{sub_ext}")
        paths = subprocess.check_output(["find", ext]).decode().strip().split('\n')
        

