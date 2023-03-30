#!/usr/bin/python3

import asyncio
import os
import time
import shutil
import ipaddress

# Read in a list of IPs/FQDNs from ips.txt
with open('ips.txt', 'r') as file:
    ips = [line.strip() for line in file]

# method for pinging an ipv4 host
async def ping(host):
    proc = await asyncio.create_subprocess_shell(f"ping -c 1 -W .5 {host}",
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return host, proc.returncode == 0

# method for pinging an ipv6 host
async def ping6(host):
    proc = await asyncio.create_subprocess_shell(f"ping6 -c 1 -i .5 {host}",
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return host, proc.returncode == 0

# method for determining if an address is ipv6 or not. Needed for separation of IPs in main function
def is_valid_ipv6_address(address):
    try:
        ipaddress.IPv6Address(address)
        return True
    except ipaddress.AddressValueError:
        return False

async def main():

    # method for counting backwards in an array to find the last change
    # example [0, 0, 0, 0, 0, 1, 1, 1,] the last change was '4' appends ago
    def find_last_change(arr):
        last_element = arr[-1]
        for i in range(len(arr)-2, -1, -1):
            if arr[i] != last_element:
                return len(arr)-i-1
            last_element = arr[i]
        return 0

    # make a dictionary/hash for storying the ping history of all hosts
    ping_history = {}
    for ip in ips:
        ping_history[ip] = []

    # separate the ips array into 2 distinct arrays for ipv4 and ipv6
    ip6s = []
    ip4s = []
    for ip in ips:
        if is_valid_ipv6_address(ip):
            ip6s.append(ip)
        else:
            ip4s.append(ip)

    # forever loop until KeyboardInterrupt is caught
    while True:
        
        # create a blank results/tasks array. Go through every host in ip4s and ip6s and add to
        # the tasks array. Then trigger the tasks, putting the results into  the results array
        results = []
        tasks = []
        for host in ip4s:
            tasks.append(ping(host))
        for host in ip6s:
            tasks.append(ping6(host))
        results = await asyncio.gather(*tasks)

        # iterate through results, and sort the ping fails from ping successes, and update the
        # corresponding dicitonary mapping for that host in ping_history
        for result in results:
            this_host = result[0]
            this_result = result[1]
            if this_result:
                ping_history[this_host].append(1)
            else:
                ping_history[this_host].append(0)

        # Clear the screen
        os.system('clear')
        terminal_size = shutil.get_terminal_size((80, 24))

        # make sure terminal width is wide enough to print output (will continue to ping if width is too narrow)
        # and once user widens terminal window resume normal output.
        if terminal_size.columns < 59:
            print("\u250C" + ('\u2500' * (terminal_size.columns - 2)) + "\u2510")
            print(" Please\n Increase\n Terminal\n Width\n Minimum Cols: 59")
            print("\u2514" + ('\u2500' * (terminal_size.columns - 2)) + "\u2518")
        else:
            print("\u250C" + ('\u2500' * (terminal_size.columns - 2)) + "\u2510")
            print(' ' * int((terminal_size.columns / 2) -13), "Welcome to nelliePing v5.9!")
            print(' ' * (terminal_size.columns -13)," Last")
            print(" Host:",' ' * (terminal_size.columns - 19),"Change")
            print( '\u255e' + '\u2550' * (terminal_size.columns -13) + "\u256a" + ('\u2550' * 10) + '\u2561')

            for ip in ips:
                last_change_index = find_last_change(ping_history[ip])
                ip_history = "".join(['\u2588' if x == 1 else "\u25E6" for x in ping_history[ip][-(terminal_size.columns-58):]])
                change_spacing = ' '*((terminal_size.columns - 58)-len(ip_history))
                # Print the ping history for the current IP address
                print(f' {ip[0:39]:<42} [{ip_history}]{change_spacing} {last_change_index}')
            if ip6s:
                print('\n IPv6 Link-Local Addresses Currently Not Supported\n')
            print(' ' * (terminal_size.columns - 31),"Copyright @TheWiFiNinja 2023")
            print("\u2514" + ('\u2500' * (terminal_size.columns - 2)) + "\u2518")
            print("\n")

# execute the program, with ability to capture 'ctrl-c' from user to exit gracefully
if __name__ ==  '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n  Thank you for using nelliePing!\n\n")