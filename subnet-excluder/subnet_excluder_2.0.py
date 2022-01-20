#!/usr/bin/python3

import ipaddress
import re
import os

os.system('clear')
print("\n|=====================================================================|")
print("                      Welcome to Subnet Excluder v2.0!")
print("|=====================================================================|")

while True:
	print('')
	print('  Enter your supernet in the format 10.10.0.0/20')
	ipNetwork = input('\n    Enter the supernet: ')
	if re.match("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:3[1-2]|2[0-9]|1[0-9]|[0-9])$", ipNetwork):
		break

while True:
	print('\n')
	print('  Enter the comma separated network(s) you wish to exclude ')
	print('  in the format 10.10.5.50/31:')
	excludeHosts = input('\n    Network(s) to exclude: ')
	if re.match("^(?:(?:(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:3[1-2]|2[0-9]|1[0-9]|[0-9])\,)*)(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:3[1-2]|2[0-9]|1[0-9]|[0-9])$" ,excludeHosts):
		break

superNet = ipaddress.ip_network(ipNetwork)
subnets = excludeHosts.split(',')
subnetCount = len(subnets)
blockList = []
blockList.append(superNet)

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