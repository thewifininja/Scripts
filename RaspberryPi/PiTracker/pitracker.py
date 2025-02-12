#!/usr/bin/python3

import subprocess
import requests
import json
import sys
import re


def rxg_get(path):
	full_path = base_url + path + "/index.json?api_key=" + api_key
	response = json.loads(requests.get(full_path).text)
	return response

def rxg_put(path, body):
	full_path = base_url + path + '.json?api_key=' + api_key
	response = requests.put(full_path, data = body, headers = json_headers)
	return

def rxg_post(path, body):
	full_path = base_url + path + '/create.json?api_key=' + api_key
	response = requests.post(full_path, data = body, headers = json_headers)
	return

def get_current_custom_keys():
	response = rxg_get('/custom_data_keys')
	return response

def get_current_custom_sets():
	response = rxg_get('/custom_data_sets')
	return response

def does_current_hostname_exist(hname):
	current_keys = get_current_custom_keys()
	for i in current_keys:
		if i['name'].strip() == hname.strip():
			return i['id']
	return 0

def get_data_set_id():
	current_sets = get_current_custom_sets()
	for i in current_sets:
		if i['name'].strip() == "PiTracker-Pis".strip():
			return i['id']
	response = create_new_data_set()
	return response 

def update_existing_key(key):
	key_path = '/custom_data_keys/update/' + str(key)
	key_data_unformatted = {"record":{"value_text":inets_lldp, "custom_data_set_id":data_set_id}}
	key_data = json.dumps(key_data_unformatted)
	response = rxg_put(key_path, key_data)
	return

def create_new_key():
	key_path = '/custom_data_keys'
	new_record_unformatted = {"record":{"name":hostname, "value_text":inets_lldp, "custom_data_set_id":data_set_id}}
	new_record = json.dumps(new_record_unformatted)
	response = rxg_post(key_path, new_record)
	return

def create_new_data_set():
	key_path = '/custom_data_sets'
	new_record_unformatted = {"record":{"name":"PiTracker-Pis"}}
	new_record = json.dumps(new_record_unformatted)
	response = rxg_post(key_path, new_record)
	return response

ifconfig = subprocess.check_output('ifconfig').decode("utf-8")
iflist = ifconfig.split('\n')
inets = []
for i in iflist:
	if re.search(r"inet (?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", i):
		inet_stripped = re.findall('inet \d+\.\d+\.\d+\.\d+', i)
		inets.append(inet_stripped[0])
inetstring = "\n".join(inets)
lldp_neighbors = subprocess.run('sudo lldpcli show neighbors', capture_output=True, shell=True).stdout.decode()
inets_lldp = inetstring + "SPLITHERE" + lldp_neighbors



hostname = subprocess.check_output('hostname').decode("utf-8").strip()
json_headers = {'Content-Type':"application/json"}

if len(sys.argv) != 3:
	print('\n\n   PLEASE USE THE FOLLOWING FORMAT:')
	print('     pitracker.py fully.qualified.domain.name api_key\n\n')
	quit()

fqdn = sys.argv[1]
api_key = sys.argv[2]
base_url = 'https://' + fqdn + '/admin/scaffolds'
data_set_id = int(get_data_set_id())

existing_key_id = does_current_hostname_exist(hostname)

if existing_key_id:
	update_existing_key(existing_key_id) 
else:
	create_new_key()