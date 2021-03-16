"""

jarvis.py nmap default 10.10.10.100
jarvis.py nmap fast 10.10.10.100

nmap default (nmap -sC -sV -p- -vvv -A -oN nmap/default.nmap -oX nmap/default.xml <ip>)
nmap fast (nmap -p- -vvv -oN nmap/fast.nmap -oX nmap/fast.xml <ip>)

"""
import os
from pathlib import Path
from argparse import ArgumentParser

def add_parser(sub_parsers: ArgumentParser) -> None:
	nmap_parser = sub_parsers.add_parser("nmap")
	nmap_parser.add_argument("mode", help="test", choices=["default", "fast", "udp"])
	nmap_parser.add_argument("-t", "--target", help="Target IP (default is the active target, if present)", dest="target", default="127.0.0.1")
	nmap_parser.add_argument("-o --output", help="Output directory (default is ./nmap)", dest="output_dir", default="./nmap")

def main(mode: str, target: str, output_dir: str):
	output_dir = Path(output_dir)
	print(output_dir)
	if mode == "default":
		_default_nmap_scan(target, output_dir)
	elif mode == "fast":
		_fast_nmap_scan(target, output_dir)
	elif mode == "udp":
		_udp_nmap_scan(target, output_dir)


def _default_nmap_scan(target: str, output_dir: Path) -> None:
	os.system("nmap -sC -sV -p- -vvv -A -oN nmap/")

def _fast_nmap_scan(target: str, output_dir: Path) -> None:
	os.system("nmap -sC -sV -p- -vvv -A -oN nmap/")

def _udp_nmap_scan(target: str, output_dir: Path) -> None:
	os.system("nmap -sU -p- -vvv -oN nmap/")
