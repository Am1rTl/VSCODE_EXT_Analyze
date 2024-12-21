import json
import time
import requests

def find_key_by_hash(data_dict, target_hash):
    for key, hashes in data_dict.items():
        if target_hash in hashes:
            return key
    return None

def get_report_by_url(url):
    response = requests.get(f"https://www.filescan.io/api/scan/{flow_id}/report")
    
    if response.text == "Internal Server Error":
        return None
    else:
        report = json.loads(response.text)
        return report

with open("reports/filescan_reports", 'r') as f:
    data = f.read()

hash_reports = eval(data)
report_name = {}

for name in hash_reports.keys():
    report_name[name] = ''
    for flow_id in hash_reports[name]:
        report = get_report_by_url(f"https://www.filescan.io/api/scan/{flow_id}/report")

        if report is not None:
            while report['state'] != 'finished':
                time.sleep(10)
                report = get_report_by_url(f"https://www.filescan.io/api/scan/{flow_id}/report")
            
            try:
                verdict = report["sourceArchive"]["verdict"]

                if verdict != "no_threat" and verdict != "unknown":
                    if report_name[name] == '':
                        report_name[name] = verdict
                    elif report_name[name] == "suspicious":
                        report_name[name] = verdict
                    elif report_name[name] == "likely_malicious" and verdict != "malicious":
                        report_name[name] = verdict
                    elif verdict == "malicious":
                        report_name[name] = verdict

            except:
                continue

for name in report_name.keys():
    if report_name[name] != '':
        print(f"{name} - {report_name[name]}")
