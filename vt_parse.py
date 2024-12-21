import hashlib
import os
import vt

def find_name_by_hash(d, value):
    for key, val in d.items():
        if val == value:
            return key
    return None

client = vt.Client("my token")

with open("all.zip", "rb") as f:
    hash = hashlib.sha1(f.read()).hexdigest()
file = client.get_object(f"/files/{hash}")

analyze = file.last_analysis_stats

all_checkers = sum(analyze.values())
print("All checkers: ", all_checkers)
print("Malicious: ", analyze['malicious'])
print("Suspicious: ", analyze['suspicious'])
print("Undetected: ", analyze['undetected'])
print()

zip_hash = {}
hash_analyze = {}
if analyze['malicious'] > 0:
    zips = [zip for zip in os.listdir() if zip.endswith(".zip") and zip != "all.zip"]

    for zip in zips:
        with open(zip, "rb") as f:
            hash = hashlib.sha1(f.read()).hexdigest()
        zip_hash[zip] = hash

    for i in zip_hash.values():
        hash_analyze[i] = client.get_object(f"/files/{i}").last_analysis_stats

count = 0
for i in hash_analyze.keys():
    if hash_analyze[i]['malicious'] != 0 or hash_analyze[i]['suspicious'] != 0:
        extension_name = find_name_by_hash(zip_hash, i)
        if count == 0:
            print("FOUND MALWARE EXTENSION:\n")
            count += 1
        print(extension_name[:-4])
        if hash_analyze[i]['malicious'] != 0:
            print(f"    Malicious detects: {hash_analyze[i]['malicious']}")
        if hash_analyze[i]['suspicious'] != 0:
            print(f"    Malicious detects: {hash_analyze[i]['suspicious']}")
        print('')

client.close()
