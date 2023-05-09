#!/usr/bin/python3

import asyncio
import os
import time

# Read in a list of IPs/FQDNs from ips.txt
with open('ips.txt', 'r') as file:
    ips = [line.strip() for line in file]


async def ping(host):
    proc = await asyncio.create_subprocess_shell(f"ping -c 1 -W .5 {host}",
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return host, proc.returncode == 0


async def main():

    def find_last_change(arr):
        last_element = arr[-1]
        for i in range(len(arr)-2, -1, -1):
            if arr[i] != last_element:
                return len(arr)-i-1
            last_element = arr[i]
        return 0

    ping_history = {}
    for ip in ips:
        ping_history[ip] = []

    while True:
        
        results = []
        tasks = [ping(host) for host in ips]
        results = await asyncio.gather(*tasks)

        for result in results:
            this_host = result[0]
            this_result = result[1]
            if this_result:
                ping_history[this_host].append(1)
            else:
                ping_history[this_host].append(0)

        # Clear the screen
        os.system('clear')

        print("|=============================================================================================================|")
        print("                                         Welcome to nelliePing v4.0!")
        print("|=============================================================================================================|")
        print("             History: 60 Pings")
        print("\t                                                                                          Last")
        print("\t Host:                     1        10        20        30        40        50        60  Change")
        print("\t---------------------------|--------|---------|---------|---------|---------|---------|---|---------")

        for ip in ips:
            last_change_index = find_last_change(ping_history[ip])
            ip_history = "".join(["X" if x == 1 else "-" for x in ping_history[ip][-60:]])
            change_spacing = ' '*(62-len(ip_history))
            # Print the ping history for the current IP address
            print(f'\t{ip[0:20]:<25} [{ip_history}]{change_spacing}{last_change_index}')

        print("\n|=============================================================================================================|")
        print("                                                                    Copyright @TheWiFiNinja 2023")
        print("|=============================================================================================================|")
        print("\n")

        # Wait for 1 second before pinging again
        #time.sleep(1)


if __name__ ==  '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n  Thank you for using nelliePing!\n\n")