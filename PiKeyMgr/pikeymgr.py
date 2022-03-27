#!/usr/bin/python3

import subprocess
import requests
import json
import sys

# Put your keyfile path, and desired admin roles here:
keyfile_path = "/Users/nkarrick/.ssh/authorized_keys"
admin_roles_to_import = [
	"Super User"
]

def rxg_get(path):
	full_path = base_url + path + "/index.json?api_key=" + api_key
	response = json.loads(requests.get(full_path).text)
	return response

def get_ssh_keys():
	response = rxg_get('/ssh_keypairs')
	return response

def get_admin_roles():
	response = rxg_get('/admin_roles')
	return response

if len(sys.argv) != 3:
	print('\n\n   PLEASE USE THE FOLLOWING FORMAT:')
	print('     pikeymgr.py fully.qualified.domain.name api_key\n\n')
	quit()

fqdn = sys.argv[1]
api_key = sys.argv[2]
base_url = 'https://' + fqdn + '/admin/scaffolds'
current_keys = []

admin_roles = get_admin_roles()
admin_role_ids = []

for i in admin_roles:
	if i['name'] in admin_roles_to_import:
		admin_role_ids.append(i['id'])

current_key_pair_data = get_ssh_keys()

for i in current_key_pair_data:
	if i['admin']['admin_role_id'] in admin_role_ids:
		current_keys.append(i["public_key"])

keyfile = open(keyfile_path, "a+")

for i in current_keys:
	keyfile.seek(0)
	if (i in keyfile.read()):
		print("Key Exists")
	else:
		keyfile.write("\n" + i)

keyfile.close()