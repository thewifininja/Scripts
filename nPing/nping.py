#!/usr/bin/python3

import os
import platform
import subprocess
import sys

def newping(host):
	with open(os.devnull, "wb") as limbo:
		result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "1", host],
			stdout=limbo, stderr=limbo).wait()
		if result == 0:
			return 1
		else:
			return 0

def printOut():
	for j in range(1,10000):
		for i in hosts:
			testping = newping(i)
			hostshash[i].append(testping)
		os.system('clear')
		print("\n")
		print("|===============================================================|")
		print("                      Welcome to nelliePing!")
		print("|===============================================================|\n")
		print("  Host                      Attempts   Answers     Average")
		print("  ----                      --------   -------     -------")
		for i in hosts:
			attempts = str(len(hostshash[i]))
			answers = str(hostshash[i].count(1))
			average = sum(hostshash[i]) / int(attempts)
			print(" ", i + (' '* (28-len(i))), attempts + (' '* (10-len(attempts))), answers + (' '* (10-len(answers))), round(average, 3))

		print("\n|===============================================================|")
		print("   Copyright STEP CG LLC 2021")
		print("|===============================================================|")
		print("\n")
		

hosts = [ ]

# hosts = [
# 	'8.8.8.8',
# 	'8.1.4.2',
# 	'8.8.4.4',
# 	'10.103.2.144'
# ]
# 
hostshash = {}

with open(sys.argv[1]) as filename:
	for line in filename:
		hosts.append(line.strip())


for i in hosts:
	hostshash[i] = []

# print(hostshash)
printOut()


