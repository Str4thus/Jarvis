

jarvis.py nmap default 10.10.10.100
jarvis.py nmap fast 10.10.10.100

nmap default (nmap -sC -sV -p- -vvv -A -oN nmap/default.nmap -oX nmap/default.xml <ip>)
nmap fast (nmap -p- -vvv -oN nmap/fast.nmap -oX nmap/fast.xml <ip>)


