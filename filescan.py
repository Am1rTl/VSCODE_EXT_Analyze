import os
import subprocess
import requests
import zipfile

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

temp_dir = subprocess.check_output(['mktemp', '-d']).decode('utf-8').strip()
for user in users:
    for ext_name in extensions[f"/home/{user}/.vscode/extensions"]:
        os.makedirs(os.path.join(temp_dir, user, ext_name), exist_ok=True)
        ext_files = subprocess.run(['find', f'/home/{user}/.vscode/extensions/{ext_name}', '-type', 'f'], capture_output=True, text=True).stdout.splitlines()
        for file in ext_files:
            rash = file.split('.')[-1:][0]
            try:
                if len(rash) < 6:
                    try:
                        with open(os.path.join(temp_dir, user, ext_name, "file."+rash), 'a') as f:
                            with open(file, 'r') as e:
                                f.write(str(e.read())[2:-1]+"\n")
                    except:
                        with open(os.path.join(temp_dir, user, ext_name, "file."+rash), 'a') as f:
                            with open(file, 'rb') as e:
                                f.write(str(e.read())[2:-1]+"\n")
                else:
                    raise Exception("File name too long")
            except:
                with open(os.path.join(temp_dir, user, ext_name, "file.txt"), 'a') as f:
                    with open(file, 'rb') as e:
                        f.write(str(e.read())[2:-1]+"\n")

os.system(f"rm -rf {temp_dir}/*/*/*.png")
os.system(f"rm -rf {temp_dir}/*/*/*.PNG")
os.system(f"rm -rf {temp_dir}/*/*/*.JPG")
os.system(f"rm -rf {temp_dir}/*/*/*.jpg")
os.system(f"rm -rf {temp_dir}/*/*/*.GIF")
os.system(f"rm -rf {temp_dir}/*/*/*.gif")

for user in users:
    ext = subprocess.check_output(['ls', f"{temp_dir}/{user}"]).decode('utf-8').strip().split("\n")
    for e in ext:
        path = f"{temp_dir}/{user}/{e}"
        ext_files = ext = subprocess.check_output(['ls', path]).decode('utf-8').strip().split("\n")

        count = 0
        for file in ext_files:
            with zipfile.ZipFile(f"{path}/arch{count//5}.zip", 'a') as zip_file:
                zip_file.write(path+'/'+file)
            count += 1  

ext_hash = {}

for user in users:
    ext = subprocess.check_output(['ls', f"{temp_dir}/{user}"]).decode('utf-8').strip().split("\n")
    for e in ext:
        path = f"{temp_dir}/{user}/{e}"
        ext_zips = ext = subprocess.check_output(['ls', path]).decode('utf-8').strip().split("\n")
        for temp in ext_zips[:]:
            if not temp.endswith(".zip"):
                ext_zips.remove(temp)
        ext_hash[e] = []

        for zip in ext_zips:
            zip_path = f"{temp_dir}/{user}/{e}/{zip}"
            url = "https://www.filescan.io/api/scan/file"
            headers = {
                "User -Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "ru,en;q=0.5",
                "Origin": "https://www.filescan.io",
                "Referer": "https://www.filescan.io/scan",
            }
            files = {
                'file': (zip, open(zip_path, 'rb'), 'application/zip'),
            }
            data = {
                'description': '',
                'tags': '',
                'password': '',
                'save_preset': 'false',
                'propagate_tags': 'true',
                'is_private': 'false',
                'skip_whitelisted': 'false',
                'rapid_mode': 'false',
                'osint': 'true',
                'extended_osint': 'true',
                'extracted_files_osint': 'true',
                'visualization': 'true',
                'files_download': 'true',
                'resolve_domains': 'true',
                'input_file_yara': 'true',
                'extracted_files_yara': 'true',
                'whois': 'true',
                'ips_meta': 'true',
                'images_ocr': 'true',
            }
            response = requests.post(url, headers=headers, files=files, data=data)
            try:
                ext_hash[e].append(response.json()['flow_id'])
            except:
                try:
                    zip_path = f"{temp_dir}/{user}/{e}/{zip}"
                    url = "https://www.filescan.io/api/scan/file"
                    headers = {
                        "User -Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Language": "ru,en;q=0.5",
                        "Origin": "https://www.filescan.io",
                        "Referer": "https://www.filescan.io/scan",
                    }
                    files = {
                        'file': (zip, open(zip_path, 'rb'), 'application/zip'),
                    }
                    data = {
                        'description': '',
                        'tags': '',
                        'password': '',
                        'save_preset': 'false',
                        'propagate_tags': 'true',
                        'is_private': 'false',
                        'skip_whitelisted': 'false',
                        'rapid_mode': 'false',
                        'osint': 'true',
                        'extended_osint': 'true',
                        'extracted_files_osint': 'true',
                        'visualization': 'true',
                        'files_download': 'true',
                        'resolve_domains': 'true',
                        'input_file_yara': 'true',
                        'extracted_files_yara': 'true',
                        'whois': 'true',
                        'ips_meta': 'true',
                        'images_ocr': 'true',
                    }
                    response = requests.post(url, headers=headers, files=files, data=data)
                    files['file'][1].close()
                    ext_hash[e].append(response.json()['flow_id'])
                except:
                    print("Can`t resend file.")

try:
    with open("reports/filescan_reports", 'w') as f:
        f.write(str(ext_hash)) 
except:
    os.system("touch reports/filescan_reports")
    with open("reports/filescan_reports", 'w') as f:
        f.write(str(ext_hash))
