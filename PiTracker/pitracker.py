#!/usr/bin/python3

import subprocess
import requests
import json
import sys


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

def does_current_hostname_exist(hname):
	current_keys = get_current_custom_keys()
	for i in current_keys:
		if i['name'].strip() == hname.strip():
			return i['id']
	return 0

def update_existing_key(key):
	key_path = '/custom_data_keys/update/' + str(key)
	key_data_unformatted = {"record":{"value_text":ifconfig}}
	key_data = json.dumps(key_data_unformatted)
	response = rxg_put(key_path, key_data)
	return

def create_new_key():
	key_path = '/custom_data_keys'
	new_record_unformatted = {"record":{"name":hostname, "value_text":ifconfig}}
	new_record = json.dumps(new_record_unformatted)
	response = rxg_post(key_path, new_record)
	return

if 'win32' not in sys.platform:
	ifconfig = subprocess.check_output('ifconfig').decode("utf-8")
else:
	ifconfig = subprocess.check_output('ipconfig').decode("utf-8")

hostname = subprocess.check_output('hostname').decode("utf-8")
json_headers = {'Content-Type':"application/json"}

if len(sys.argv) != 3:
	print('\n\n   PLEASE USE THE FOLLOWING FORMAT:')
	print('     pitracker.py fully.qualified.domain.name api_key\n\n')
	quit()

fqdn = sys.argv[1]
api_key = sys.argv[2]
base_url = 'https://' + fqdn + '/admin/scaffolds'

existing_key_id = does_current_hostname_exist(hostname)

if existing_key_id:
	update_existing_key(existing_key_id) 
else:
	create_new_key()