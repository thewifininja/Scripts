#!/opt/homebrew/bin/python3

import requests
import sys 
import csv
import json

def device_update(hostname, update_request):
    api_url = "https://{}/api/v0/devices/{}".format(fqdn, hostname)
    r = requests.patch(api_url, data=json.dumps(update_request), headers=request_headers)

def find_or_create_a_location(loc_data):
    locations_url = "https://{}/api/v0/resources/locations".format(fqdn)
    existing_locations = json.loads(requests.get(locations_url, headers=request_headers).text)
    api_url = "https://{}/api/v0/locations".format(fqdn)
    keep_looking = True
    location_id = 0
    #cycle through locations looking for a match
    for i in existing_locations['locations']:
        if i['location'] == loc_data['location']:
            keep_looking = False
            location_id = i['id']
    if location_id == 0:
        response = json.loads(requests.post(api_url, data=json.dumps(loc_data), headers=request_headers).text)
        location_id = response['message'].split('#')[1]
    return location_id

if len(sys.argv) != 4:
    print('\n\n   PLEASE USE THE FOLLOWING FORMAT:')
    print('     ./location_update <csv_filename> <fqdn/ip> <api_key>\n\n')
    quit()

csv_input = sys.argv[1]
fqdn = sys.argv[2]
api_key = sys.argv[3]

# Setup Requests Headers
request_headers = {"Content-Type": "application/json",
                   "Accept-Language": "en-US,en;q=0.5",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "X-Auth-Token": api_key,
                   "Connection": "keep-alive"
                   }


# Read CSV file
csv_file = open(csv_input, mode='r')
csv_reader = csv.DictReader(csv_file)

for row in csv_reader:
    loc_data = {"location":row['location'], "lat":row['lat'], "lng":row['long']}
    loc_id = find_or_create_a_location(loc_data)
    update_request = {"field": "location_id", "data": loc_id}
    device_update(row['hostname'], update_request)
quit()