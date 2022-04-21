#!/usr/bin/python3

import os
import platform
import subprocess
import sys
import paramiko
import time

def sshJob(server, uname, pword, cmds):
	cmdsToRun = cmds.split('\n')
	#print(cmdsToRun)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	keepGoing = 0
	try:
		ssh.connect(server, 22, uname, pword, allow_agent=False, look_for_keys=False, timeout=5)
		commands = ssh.invoke_shell()
		keepGoing = 1
	except:
		hostshash[server] = 'FAILED'
	if keepGoing:	
		try:
			commands.send(chr(25)) # used for sending ctrl-y on avaya switches
			for i in cmdsToRun:
				cmdWithNewLine = i + "\n"
				commands.send(cmdWithNewLine)
				time.sleep(1)
			hostshash[server] = 'Complete'
		except:
			hostshash[server] = 'FAILED'
	else:
		hostshash[server] = 'FAILED'

hosts = [ ]
 
hostshash = {}

argFile = sys.argv[1]

with open(argFile) as filename:
	for line in filename:
		hosts.append(line.strip())

for i in hosts:
	hostshash[i] = 'Pending'

os.system('clear')
print("\n\n")
usernameInput = input(" Enter the SSH username: ")
passwordInput = input(" Enter the SSH password: ")
print(" Input your commands. Finish with blank line: \n")
linesOfInput = []
while True:
    line = input()
    if line:
        linesOfInput.append(line)
    else:
        break
commands = '\n'.join(linesOfInput)

for i in hosts:
	result = sshJob(i, usernameInput, passwordInput, commands)
	os.system('clear')
	print("\n")
	print("|===============================================================|")
	print("                      Welcome to MultiSSH v1.0!")
	print("|===============================================================|\n")
	print("    Host                                      Status")
	print("    ----                                      ------")

	for i in hosts:
		print("   ", i, (' '* (40-len(i))), hostshash[i])
	#print("   Username:", usernameInput)
	#print("   Password:", passwordInput)
	#print("   Commands:", linesOfInput)
	#print("   hosthash:", hostshash)

	print("\n|===============================================================|")
	print("                                    Copyright STEP CG LLC 2021")
	print("|===============================================================|")
	print("\n")
