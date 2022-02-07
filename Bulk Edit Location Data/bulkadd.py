#!/usr/bin/python
import config
import math
import requests
import pandas as pd

# Setup Requests Headers
request_headers = {"Content-Type": "application/json",
                   "Accept-Language": "en-US,en;q=0.5",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "X-Auth-Token": config.librenms_apikey,
                   "Connection": "keep-alive"
                   }

def device_update(hostname, update_request):
    api_url = "http://{}/api/v0/devices/{}".format(config.librenms_ipaddress, hostname)
    r = requests.patch(api_url, json=update_request, headers=request_headers)
    print(r.text)

# Read CSV file
try:
    df = pd.read_csv("bulkadd1.csv")
except FileNotFoundError:
    print("ERROR: bulkadd.csv missing")
    quit()

for index, row in df.iterrows():
        # Add Device to LibreNMS via SNMP
    add_device = {
        "force_add":"true",
        "hostname":row['hostname'],
        "version" :['v3'],
        "authlevel":['authPriv'],
        "auth_name":[''],
        "overide_sysLocation":[1],
        "auth_pass":[''],
        "authalgo":['SHA'],
        "cryptopass":[''],
        "cryptoalgo":['AES'],
        "location_id":row['location_id'],
        "location":row['location'],
        "lat":row['lat'],
        "lng":row['lng'],
        }
    device_update("hostname", "update_request")
quit()