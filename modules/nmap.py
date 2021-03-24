import os
import time
from pathlib import Path
from argparse import ArgumentParser
from core.brain import get_brain_value

def add_parser(sub_parsers: ArgumentParser) -> None:
	nmap_parser = sub_parsers.add_parser("nmap")
	nmap_parser.add_argument("mode", help="Scan mode", choices=["default", "fast", "udp"])
	nmap_parser.add_argument("-t", "--target", help="Target IP (default is the active target, if configured)", dest="target", default=get_brain_value("target"))


	default_nmap_dir = str(Path(get_brain_value("box_dir")) / "nmap") if get_brain_value("box_dir") else None
	nmap_parser.add_argument("-o --output", help="Output directory (default is ./nmap)", dest="output_dir", default=default_nmap_dir)

def main(mode: str, target: str=None, output_dir: str=None) -> None:
	if not get_brain_value("active"):
		print("This module is only available in a valid session!")
		exit(1)

	if not target:
		print("Please specify a target via the --target switch or via 'jarvis.py brain target <ip>''")
		exit(1)

	output_dir = Path(output_dir)
	if mode == "default":
		_default_nmap_scan(target, output_dir)
	elif mode == "fast":
		_fast_nmap_scan(target, output_dir)
	elif mode == "udp":
		_udp_nmap_scan(target, output_dir)


def _default_nmap_scan(target: str, output_dir: str) -> None:
	_scan(f"nmap -sC -sV -p- -vvv -A {target}", output_dir, "default.nmap")

def _fast_nmap_scan(target: str, output_dir: Path) -> None:
	_scan(f"nmap -p- -vvv {target}", output_dir, "fast.nmap")

def _udp_nmap_scan(target: str, output_dir: Path) -> None:
	_scan(f"nmap -sU -p- -vvv {target}", output_dir, "upd.nmap")


def _scan(command, output_dir, filename):
	if os.path.isdir(output_dir):
		os.system(command + f"-oN {output_dir}/{filename}")
		return

	print("WARNING: Jarvis won't log this nmap scan. Please create a directory called 'nmap' in the box directory to fix this.")
	time.sleep(3)
	os.system(command)
