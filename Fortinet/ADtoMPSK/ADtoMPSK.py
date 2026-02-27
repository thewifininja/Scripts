import requests

def parseMPSKs(raw_data):
	alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	keys = {}
	for letter in alphabet:
		keys["student_" + letter] = []
		keys["staff_" + letter] = []
	for group in raw_data:
		for letter in alphabet:
			this_stu_group = "student_" + letter
			this_staff_group = "staff_" + letter
			if this_stu_group in group["name"]:
				for key_data in group["mpsk-key"]:
					this_key = key_data['name']
					keys[this_stu_group].append(this_key)
			if this_staff_group in group["name"]:
				for key_data in group["mpsk-key"]:
					this_key = key_data['name']
					keys[this_staff_group].append(this_key)
	return keys

def getCurrentMPSKs(url_base, get_headers):
	try:
		response = requests.get(url_base, headers=get_headers, verify=False)
		response.raise_for_status()
		parsedMPSKs = parseMPSKs(response.json()["results"][0]["mpsk-group"])
		return parsedMPSKs
	except requests.exceptions.RequestException as e:
		print(f"Error fetching data: {e}")
		return None

def createDiff(currentMPSKs, currentUsers):
	alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	# mods = {"staff_create":[], "staff_delete":[], "student_create":[], "student_delete":[]}
	mods = {}
	for letter in alphabet:
		mods["staff_" + letter + "_create"] = list(set(currentUsers["staff_" + letter]) - set(currentMPSKs["staff_" + letter]))
		mods["staff_" + letter + "_delete"] = list(set(currentMPSKs["staff_" + letter]) - set(currentUsers["staff_" + letter]))
		mods["student_" + letter + "_create"] = list(set(currentUsers["student_" + letter]) - set(currentMPSKs["student_" + letter]))
		mods["student_" + letter + "_delete"] = list(set(currentMPSKs["student_" + letter]) - set(currentUsers["student_" + letter]))
	keys_to_remove = [key for key, value in mods.items() if not value]
	for key in keys_to_remove:
		del mods[key]
	return mods

def getCurrentUsers():
	alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	users = {}
	for letter in alphabet:
		users["staff_" + letter] = []
		users["student_" + letter] = []
	student_users = ["wmorrisdean", "tmorrisdean","zrmorrisdean", "skarrick", "rkarrick"]
	staff_users = ["nkarrick", "mkarrick", "zmorrisdean", "gmorrisdean"]
	for u in student_users:
		users["student_" + u[0]].append(u)
	for u in staff_users:
		users["staff_" + u[0]].append(u)
	return users

def createKey(user, mpsk_group):
	return

def deleteKey(user, mpsk_group):
	return

def makeChanges(changes, currentMPSKs):
	# {'staff_g_create': ['gmorrisdean'], 'staff_m_create': ['mkarrick'], 'staff_n_create': ['nkarrick'], 'student_r_create': ['rkarrick'], 'student_s_delete': ['somekey', 'sremy'], 'student_t_create': ['tmorrisdean'], 'student_w_create': ['wmorrisdean'], 'staff_z_create': ['zmorrisdean'], 'student_z_create': ['zrmorrisdean']} 
	return

def main():
	hostname = "10.203.0.1"
	admin_port = "443"
	api_key = "q4nxj1rm94pkgqzrjGz3Hd36hGfqQ6"
	mpsk_group = "ADtoMPSK"
	url_base = f"https://{hostname}:{admin_port}/api/v2/cmdb/wireless-controller/mpsk-profile/{mpsk_group}"
	get_headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
	currentMPSKs = getCurrentMPSKs(url_base, get_headers)
	currentUsers = getCurrentUsers()
	changes = createDiff(currentMPSKs, currentUsers)
	print("\n\n CHANGES:")
	print(changes)
	# makeChanges(changes, currentMPSKs)


if __name__ == "__main__":
    main()
