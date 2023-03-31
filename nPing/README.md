# nPing

## Overview
---
nPing is a python script designed provide the end user with a graphical interface for ICMP, while pinging multiple hosts simultaneously. The script will automatically adjust to your terminal width, with a minimum 59 columns needed for output. 

##How to use
---
make the script executable. `chmod +x nping.py`
```
./nping.py
```

Simply have a file named `ips.txt` in the same directory as the script. 

example:
```
192.168.1.1
172.16.0.1
10.0.0.1
8.8.8.8
2001:db8::1000
www.google.com
```

There is support for IPv6 (except for link-local currently).
All FQDNs are also assumed to resolve to IPv4 addresses.


