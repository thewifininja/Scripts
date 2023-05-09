#!/usr/bin/env python3

import argparse
import asyncio
import os
import time
import shutil
import ipaddress

DEFAULT_FILE = 'ips.txt'
DEFAULT_FREQ = 1

def help():
    print('\n Thank you for your interest in fnPing!\n')
    print(' If found, this script will use a file in the same directory')
    print(' named \'ips.txt\'')
    print(' The file should contain one host per line, and supports ipv4 and ipv6')
    print(' addresses. FQDNs are also supported, but limited to ipv4 currently.')
    print(' An example file might look like:\n')
    print('-----------------------------------')
    print('  8.8.8.8')
    print('  10.255.10.1')
    print('  10.84.0.1')
    print('  10.103.255.1')
    print('  10.84.0.235')
    print('  10.84.3.25')
    print('  fe80::1076:71bc:5657:bbaa')
    print('-----------------------------------\n')
    print('\n CLI parameters are also supported: \n')
    print(' -h, --help  Prints this help message.')
    print(' -p, --path  Accepts a path to a file to use other than ips.txt')
    print(' -i, --ips   Accepts comma-separated IPs to use in lieu of a text file.')
    print(' -f, --freq  Integer for frequency of pings.')
    print('\n    GOOD LUCK!\n')

# Read in a list of IPs/FQDNs from ips.txt
def load_file(file_path):
    if file_path is None:
        file_path = DEFAULT_FILE
    try:
        try:
            with open(file_path, 'r') as file:
                ips = [line.strip() for line in file]
        except:
            ips = []

            os.system('clear')
            help()
            while len(ips) < 1 or ips == ['']:
                print('\n  For convenience you can Enter IPs below, or press \'ctrl-c\' to quit')
                ips = "".join(input('  Comma separated IPs here: ').split()).split(',')
        return ips
    except KeyboardInterrupt:
        print("\n\n  Thank you for using fnPing!\n\n")
        quit()

# method for pinging an ipv4 host
async def ping(host):
    proc = await asyncio.create_subprocess_shell(f"ping -c 1 -W 1 {host}",
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return host, proc.returncode == 0

# method for pinging an ipv6 host
async def ping6(host):
    proc = await asyncio.create_subprocess_shell(f"ping6 -c 1 -i 1 {host}",
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

def get_frequency(args):
    freq = DEFAULT_FREQ
    freq_error = f'Frequency value of \'{args["freq"]}\' is invalid. Using '
    freq_error += f'default of {DEFAULT_FREQ}.'
    if args.get('freq'):
        try:
            freq = int(args['freq'])
        except ValueError:
            print(freq_error)
        if freq <= 0:
            print(freq_error)
            freq = DEFAULT_FREQ
    return freq

async def main(args):
    if args.get('help'):
       help()
       quit()

    ips = []
    if args.get('ips'):
        ips = [i.strip() for i in args['ips'].split(',')]
    else:
        ips = load_file(args.get('path'))

    if not ips:
        print('Failed to receive any IP addresses!')
        quit()

    freq = get_frequency(args)

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
    # detect if there are any ipv6 link local addresses
    link_locals = []
    for host in ip6s:
        if ipaddress.ip_address(host).is_link_local:
            link_locals.append(host)

    # creat counter for total Ping Count
    total_ping_count = 0


    # forever loop until KeyboardInterrupt is caught
    while True:
        # look to see if there are any ping failures in the last round of pinging. if not introduce
        # a 1 second delay before pinging again. This prevents ICMP DDoS. If there are ping failures
        # the ping() function has a built in wait of 1 second, so the sleep is not needed or you get
        # a 2 second ping interval
        ping_fails = 0
        for ip in ips:
            if ping_history[ip]:
                if ping_history[ip][-1] == 0:
                    ping_fails +=1

        if ping_fails == 0:
            time.sleep(freq)

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

        # increment total ping count
        total_ping_count += 1


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
            print(' ' * int((terminal_size.columns / 2) -13), "Welcome to fnPing v8!\n")
            print(' Total Pings:      ' + str(total_ping_count))
            print(' Pings Displayed:  ' + str(terminal_size.columns - 58))
            print(' ' * (terminal_size.columns -13)," Last")
            print(" Host:",' ' * (terminal_size.columns - 19), "Change")
            print( '\u255e' + '\u2550' * (terminal_size.columns -13) + "\u256a" + ('\u2550' * 10) + '\u2561')

            for ip in ips:
                if ip in link_locals:
                    print(f' {ip[0:39]:<42} [\u2573]')
                else:
                    last_change_index = find_last_change(ping_history[ip])
                    ip_history = "".join(['\u2588' if x == 1 else "\u25E6" for x in ping_history[ip][-(terminal_size.columns-58):]])
                    change_spacing = ' '*((terminal_size.columns - 58)-len(ip_history))
                    # Print the ping history for the current IP address
                    print(f' {ip[0:39]:<42} [{ip_history}]{change_spacing} {last_change_index}')
            if link_locals:
                print('\n \u2573 - IPv6 Link-Local Addresses Currently Not Supported\n')
            else:
                print('\n')
            print(' ' * (terminal_size.columns - 31),"Copyright @TheWiFiNinja 2023")
            print("\u2514" + ('\u2500' * (terminal_size.columns - 2)) + "\u2518")
            print("\n")

# execute the program, with ability to capture 'ctrl-c' from user to exit gracefully
if __name__ ==  '__main__':
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument('-h', '--help',
                            action='store_true',
                            required=False)
    arg_parser.add_argument('-p', '--path',
                            action='store',
                            required=False)
    arg_parser.add_argument('-i', '--ips',
                            action='store',
                            required=False)
    arg_parser.add_argument('-f', '--freq',
                            action='store',
                            required=False)
    arg_dict = vars(arg_parser.parse_args())
    try:
        asyncio.run(main(arg_dict))
    except KeyboardInterrupt:
        print("\n\n  Thank you for using fnPing!\n\n")
        quit()

