import requests
import pprint

def params():
	hostname = "10.203.0.1"
	admin_port = "443"
	api_key = "q4nxj1rm94pkgqzrjGz3Hd36hGfqQ6"
	mpsk_group = "ADtoMPSK"
	return hostname, admin_port, api_key, mpsk_group

def clean_dict(d):
    cleaned = {
        key: clean_dict(value) if isinstance(value, dict) else value
        for key, value in d.items()
        if not (isinstance(value, list) and not value)  # Remove empty lists
    }
    return {k: v for k, v in cleaned.items() if v}  # Remove empty dictionaries

def parseMPSKs(raw_data):
	alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	keys = {"student": {}, "staff":{}}
	for letter in alphabet:
		keys["student"][letter] = []
		keys["staff"][letter] = []
	for group in raw_data:
		for letter in alphabet:
			this_stu_group = "student_" + letter
			this_staff_group = "staff_" + letter
			if this_stu_group in group["name"]:
				for key_data in group["mpsk-key"]:
					this_key = key_data['name']
					keys["student"][letter].append(this_key)
			if this_staff_group in group["name"]:
				for key_data in group["mpsk-key"]:
					this_key = key_data['name']
					keys["staff"][letter].append(this_key)
	return keys

def getCurrentMPSKs(url_base, headers):
	try:
		response = requests.get(url_base, headers=headers, verify=False)
		response.raise_for_status()
		parsedMPSKs = parseMPSKs(response.json()["results"][0]["mpsk-group"])
		return parsedMPSKs
	except requests.exceptions.RequestException as e:
		print(f"Error fetching data: {e}")
		return None

def createDiff(currentMPSKs, currentUsers):
	alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	# mods = {"staff_create":[], "staff_delete":[], "student_create":[], "student_delete":[]}
	mods = {"create":{"staff":{},"student":{}},"delete":{"staff":{},"student":{}}}
	for letter in alphabet:
		mods["create"]["staff"][letter] = []
		mods["delete"]["staff"][letter] = []
		mods["create"]["student"][letter] = []
		mods["delete"]["student"][letter] = []
	for letter in alphabet:
		mods["create"]["staff"][letter] = list(set(currentUsers["staff"][letter]) - set(currentMPSKs["staff"][letter]))
		mods["delete"]["staff"][letter] = list(set(currentMPSKs["staff"][letter]) - set(currentUsers["staff"][letter]))
		mods["create"]["student"][letter] = list(set(currentUsers["student"][letter]) - set(currentMPSKs["student"][letter]))
		mods["delete"]["student"][letter] = list(set(currentMPSKs["student"][letter]) - set(currentUsers["student"][letter]))
	cleaned_mods = clean_dict(mods)
	return cleaned_mods

def getCurrentUsers():
	alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	users = {"student":{}, "staff":{}}
	for letter in alphabet:
		users["staff"][letter] = []
		users["student"][letter] = []
	student_users = ["wmorrisdean", "tmorrisdean","zmorrisdean", "skarrick", "rkarrick", "sskarrick"]
	staff_users = ["nkarrick", "mkarrick", "zrmorrisdean", "gmorrisdean"]
	for u in student_users:
		users["student"][u[0]].append(u)
	for u in staff_users:
		users["staff"][u[0]].append(u)
	return users

def createKey(utype, letter, user, current_keys):
	print("Create User: " + user + " in group: " + utype + "_" + letter)
	return

def deleteKey(utype, letter, user):
	print("Delete User: " + user + " from group: " + utype + "_" + letter)
	return

def makeChanges(changes, currentMPSKs):
	#{
	#	'create': {
	#		'staff':{
	#				'g': ['gmorrisdean'],
	#                'm': ['mkarrick'],
	#                'n': ['nkarrick'],
	#                'z': ['zrmorrisdean']
	#             },
	#        'student':{
	#        		'r': ['rkarrick'],
	#                't': ['tmorrisdean'],
	#                'w': ['wmorrisdean'],
	#                'z': ['zmorrisdean']
	#             }
	#    },
	#	'delete':{
	#		'student': {
	#			's': ['somekey', 'sremy']
	#		}
	#	}
	#}
	for action, action_data in changes.items():
		for utype, udata in action_data.items():
			for letter, letterdata in udata.items():
				for user in letterdata:
					if action == "create":
						createKey(utype, letter, user, currentMPSKs[utype][letter])
					elif action == "delete":
						deleteKey(utype, letter, user)
	return

def main():
	hostname, admin_port, api_key, mpsk_group = params()
	url_base = f"https://{hostname}:{admin_port}/api/v2/cmdb/wireless-controller/mpsk-profile/{mpsk_group}"
	headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
	currentMPSKs = getCurrentMPSKs(url_base, headers)
	currentUsers = getCurrentUsers()
	changes = createDiff(currentMPSKs, currentUsers)
	print("\n\n")
	makeChanges(changes, currentMPSKs)


if __name__ == "__main__":
    main()
