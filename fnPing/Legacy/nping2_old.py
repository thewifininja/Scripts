#!/usr/bin/python3

import os
import platform
import subprocess
import sys


def fping(fname):
	try:
		# subprocess = subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE)
		result=subprocess.Popen(["fping", "-f", fname, "-t", "150"], stdout=subprocess.PIPE)
		output = result.stdout.read()
		return output
	except:
		print("\n\n ERROR in fping method!\n\n")

def printOut(file):
	for j in range(1,10000):
		fpingResult = fping(file)
		fpingResultList = fpingResult.splitlines()
		for i in fpingResultList:
			results = i.split()
			thishost = results[0].decode('UTF-8')
			thisresponse = results[2].decode('UTF-8')
			if 'alive' in thisresponse:
				hostshash[thishost].append(1)
			else:
				hostshash[thishost].append(0)
		os.system('clear')
		print("\n")
		print("|===============================================================|")
		print("                      Welcome to nelliePing v2.0!")
		print("|===============================================================|\n")
		print("  Host                      Attempts   Answers     Average")
		print("  ----                      --------   -------     -------")
		for i in hosts:
			attempts = str(len(hostshash[i]))
			answers = str(hostshash[i].count(1))
			average = sum(hostshash[i]) / int(attempts)
			print(" ", i + (' '* (28-len(i))), attempts + (' '* (10-len(attempts))), answers + (' '* (10-len(answers))), round(average, 3))

		print("\n|===============================================================|")
		print("   Copyright TheWiFiNinja 2021")
		print("|===============================================================|")
		print("\n")
		

hosts = [ ]
 
hostshash = {}

argFile = sys.argv[1]

with open(argFile) as filename:
	for line in filename:
		hosts.append(line.strip())


for i in hosts:
	hostshash[i] = []

printOut(argFile)


