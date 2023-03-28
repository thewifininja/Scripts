#!/usr/bin/python3

import subprocess
import os
import time
import multiprocessing

# Read in a list of IPs/FQDNs from ips.txt
with open('ips.txt', 'r') as file:
    ips = [line.strip() for line in file]


def ping(ip, history):
    # Ping the current IP address
    ping_result = ''
    ping_process = subprocess.Popen(['ping', '-c', '1','-W', '.5', ip], stdout=subprocess.PIPE)
    output, error = ping_process.communicate()

    if '1 packets received' in str(output):
        history.append(1)
    else:
        history.append(0)


if __name__ ==  '__main__':

    ping_history = {}
    manager = multiprocessing.Manager()

    for ip in ips:
        ping_history[ip] = manager.list()

    #ping_history = {ip: multiprocessing.Manager() for ip in ips}  # Initialize a dictionary to store the ping history for each IP

    while True:
        # Spawn a new process for each IP address in the list
        processes = [multiprocessing.Process(target=ping, args=(ip,ping_history[ip])) for ip in ips]

        # Start all the processes
        for process in processes:
            process.start()

        # Wait for all the processes to finish
        for process in processes:
            process.join()

        # Clear the screen
        os.system('clear')

        print("|==============================================================================================================================|")
        print("                                                  Welcome to nelliePing v3.0!")
        print("|==============================================================================================================================|")
        print("             History: 60 Pings\n")

        for ip in ips:
            if len(ping_history[ip]) > 60:
                ping_history[ip].pop(0)
            # Print the ping history for the current IP address
            print(f'\t{ip:<50} [{"".join(["X" if x == 1 else "." for x in ping_history[ip]])}]'.replace(' ', '-'))

        print("\n|==============================================================================================================================|")
        print("                                                                                                Copyright @TheWiFiNinja 2023")
        print("|==============================================================================================================================|")
        print("\n")

        # Wait for 1 second before pinging again
        #time.sleep(1)
