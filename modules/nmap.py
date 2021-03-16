"""

jarvis.py nmap default 10.10.10.100
jarvis.py nmap fast 10.10.10.100

nmap default (nmap -sC -sV -p- -vvv -A -oN nmap/default.nmap -oX nmap/default.xml <ip>)
nmap fast (nmap -p- -vvv -oN nmap/fast.nmap -oX nmap/fast.xml <ip>)

"""

def add_parser(sub_parsers):
	nmap_parser = sub_parsers.add_parser("nmap")
	nmap_parser.add_argument("nmap1", help="test")
	nmap_parser.add_argument("nmap2", help="test")

def main(nmap1, nmap2):
    print("nmap!")
    print(nmap1, nmap2)