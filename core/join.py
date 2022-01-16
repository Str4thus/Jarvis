import os
import time
import tempfile
import socket
import fcntl
import struct
from pathlib import Path
from argparse import ArgumentParser
from modules.pwnbooks import pwnbooks_init
from .config import get_config_value
from .brain import init_session


def add_parser(sub_parsers: ArgumentParser) -> None:
	join_parser = sub_parsers.add_parser("join")
	join_parser.add_argument("lab_name", help="Kind of CTF", choices=get_config_value("configured_labs"))
	join_parser.add_argument("box_name", help="Name of the box/working directory")
	join_parser.add_argument("--release", help="Connects to the release arena on HTB", action="store_true", default=False)
	join_parser.add_argument("--subdir", help="Subdirectory to create within the working directory (useful when a CTF consists of couple daily challenges)", dest="sub_dir", default=None)
	join_parser.add_argument("--empty", help="Do not create default folders inside (nmap, gobuster, etc)", action="store_true", default=False)
	join_parser.add_argument("--vpn", help="Specify a VPN to use", dest="vpn_path", default=None)
	join_parser.add_argument("--tmp, --temp", help="Create the box directory in a temporary locaton", action="store_true", dest="is_temp", default=False)
	join_parser.add_argument("-t", "--target", help="Specify the target's ip", default=None)
	join_parser.add_argument("--pwnbooks", help="Generate notes for this box", dest="shall_init_pwnbooks", action="store_true", default=False)


def main(lab_name: str, box_name: str, release: bool=False, empty: bool=False, sub_dir: str=None, vpn_path: str=None, is_temp: bool=False,
	target: str=None, shall_init_pwnbooks: bool=False) -> None:
	if not (get_config_value(lab_name + "_vpn") or vpn_path) and not (get_config_value(lab_name + "_dir") or is_temp):
		print("Unrecognized lab! You can specify --vpn <vpn_path> and --tmp or add a new lab via 'jarvis.py labs add <lab_name>''")
		exit(1)

	if not vpn_path:
		if release:
			vpn_path = Path(get_config_value(lab_name + "_release_vpn"))
		else:
			vpn_path = Path(get_config_value(lab_name + "_vpn"))


	if is_temp:
		cwd = Path(tempfile.gettempdir()) / box_name
	else:
		cwd = Path(get_config_value(lab_name + "_dir")) / box_name
		if sub_dir:
			cwd /= sub_dir


	init_session(box_name=box_name, box_dir=cwd, vpn_path=vpn_path,
		lab_name=lab_name, target=target)
	
	if shall_init_pwnbooks:
		pwnbooks_init(lab_name, box_name)

	_create_cwd_if_not_exists(cwd, empty)
	_setup_tmux(cwd, vpn_path, shall_init_pwnbooks)
	_attach_to_tmux(cwd)

def _create_cwd_if_not_exists(cwd: Path, shall_be_empty: bool=False) -> None:
	if not os.path.exists(cwd):
		os.makedirs(cwd)

		if not shall_be_empty:
			for folder in get_config_value("default_folders"):
				os.mkdir(cwd / folder)


def _setup_tmux(cwd: Path, vpn_path: Path, shall_init_pwnbooks: bool=False) -> None:
	os.system(f"tmux new-session -d -c {cwd} -s Jarvis")

	if shall_init_pwnbooks:
		os.system(f"tmux send -t Jarvis:0 'obsidian; openvpn {vpn_path}' C-m")
	else:
		os.system(f"tmux send -t Jarvis:0 'openvpn {vpn_path}' C-m")

	time.sleep(1) # Wait for VPN connection
	os.system(f"tmux new-window -t Jarvis -c {cwd}")

def _attach_to_tmux(cwd: Path) -> None:
	os.system(f"tmux at -t Jarvis -c {cwd}")
