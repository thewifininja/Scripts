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

    stop_event = multiprocessing.Event()

    ping_history = {}
    manager = multiprocessing.Manager()

    for ip in ips:
        ping_history[ip] = manager.list()

    #ping_history = {ip: multiprocessing.Manager() for ip in ips}  # Initialize a dictionary to store the ping history for each IP

    try:
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

            print("|======================================================================================================|")
            print("                                      Welcome to nelliePing v3.0!")
            print("|======================================================================================================|")
            print("             History: 60 Pings\n")
            print("\t Host:                     1        10        20        30        40        50        60")
            print("\t---------------------------|--------|---------|---------|---------|---------|---------|--")

            for ip in ips:
                # Print the ping history for the current IP address
                print(f'\t{ip[0:20]:<25} [{"".join(["X" if x == 1 else "-" for x in ping_history[ip][-60:]])}]'.replace(' ', '_'))

            print("\n|======================================================================================================|")
            print("                                                                    Copyright @TheWiFiNinja 2023")
            print("|======================================================================================================|")
            print("\n")

            # Wait for 1 second before pinging again
            #time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()

        for process in processes:
            process.terminate()

        print("\n\n  Thank you for using nelliePing!\n\n")