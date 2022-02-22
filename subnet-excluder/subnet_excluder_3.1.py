#!/usr/bin/python3

# Import the necessary libraries
import ipaddress
import re
import os

def non_network():
	print('\n\n----------------------------------------------------')
	print('  NON-NETWORK ADDRESSES DETECTED! TRY AGAIN!')
	print('  ' + i + ' is a not a valid network address')
	print('----------------------------------------------------\n')

os.system('clear')
print("\n|=====================================================================|")
print("                      Welcome to Subnet Excluder v3.1!")
print("|=====================================================================|")

blockList = []

print('')
while True:
	print('  Enter your comma separated supernet(s) in the format 10.10.0.0/20')
	ipNetwork = input('\n    Enter the supernet(s): ')
	if ipNetwork == 'rfc1918':
		superNets = ['192.168.0.0/16','172.16.0.0/12','10.0.0.0/8']
		for i in superNets:
				net = ipaddress.ip_network(i)
				blockList.append(net)
		break
	if re.match("^(?:(?:(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:3[0-2]|2[0-9]|1[0-9]|[0-9])\,)*)(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:3[0-2]|2[0-9]|1[0-9]|[0-9])$", ipNetwork):
		superNets = ipNetwork.split(",")
		try:
			for i in superNets:
				net = ipaddress.ip_network(i)
				blockList.append(net)
			break
		except ValueError as ve:
			non_network()
print('\n')

while True:
	print('  Enter the comma separated network(s) you wish to exclude ')
	print('  in the format 10.10.5.50/31:')
	excludeHosts = input('\n    Network(s) to exclude: ')
	if re.match("^(?:(?:(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:3[0-2]|2[0-9]|1[0-9]|[0-9])\,)*)(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:3[0-2]|2[0-9]|1[0-9]|[0-9])$" ,excludeHosts):
		subnets = excludeHosts.split(',')
		try:
			for i in subnets:
				ipaddress.ip_network(i)
			break
		except ValueError as ve:
			non_network()

subnetCount = len(subnets)

for i in range(0, subnetCount):
	subnet = ipaddress.ip_network(subnets[i])
	for j in blockList:
		if subnet.subnet_of(j):
			blockList.remove(j)
			templist = list(j.address_exclude(subnet))
			for k in templist:
				blockList.append(k)

print('\n  Your remaining networks are: \n')
for i in blockList:
	print('    ' + str(i))

print('')
print("|=====================================================================|")
print("                                    Copyright STEP CG LLC 2022")
print("|=====================================================================|\n\n")