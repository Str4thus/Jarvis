import os
import time
import tempfile
import socket
import fcntl
import struct
from pathlib import Path
from .config import get_config_value
from .brain import init_session
from argparse import ArgumentParser


def add_parser(sub_parsers: ArgumentParser) -> None:
	join_parser = sub_parsers.add_parser("join")
	join_parser.add_argument("lab", help="Kind of CTF", choices=get_config_value("configured_labs"))
	join_parser.add_argument("box_name", help="Name of the box/working directory")
	join_parser.add_argument("--release", help="Connects to the release arena on HTB", action="store_true", default=False)
	join_parser.add_argument("--subdir", help="Subdirectory to create within the working directory (useful when a CTF consists of couple daily challenges)", dest="sub_dir", default=None)
	join_parser.add_argument("--empty", help="Do not create default folders inside (nmap, gobuster, etc)", action="store_true", default=False)
	join_parser.add_argument("--vpn", help="Specify a VPN to use", dest="vpn_path", default=None)
	join_parser.add_argument("--tmp, --temp", help="Create the box directory in a temporary locaton", action="store_true", dest="is_temp", default=False)
	join_parser.add_argument("-t", "--target", help="Specify the target's ip", default=None)
	join_parser.add_argument("--lhost", help="Specify lhost value", default=None)
	join_parser.add_argument("--lport", help="Specify lport value", type=int, default=31337)


def main(lab: str, box_name: str, release: bool=False, empty: bool=False, sub_dir: str=None, vpn_path: str=None, is_temp: bool=False,
	target: str=None, lhost: str=None, lport: int=None) -> None:
	if not (get_config_value(lab + "_vpn") or vpn_path) and not (get_config_value(lab + "_dir") or is_temp):
		print("Unrecognized lab! You can specify --vpn <vpn_path> and --tmp or add a new kind via 'jarvis.py labs add <lab_name>''")
		exit(1)

	if not vpn_path:
		if release:
			vpn_path = Path(get_config_value(lab + "_release_vpn"))
		else:
			vpn_path = Path(get_config_value(lab + "_vpn"))


	if is_temp:
		cwd = Path(tempfile.gettempdir()) / box_name
	else:
		cwd = Path(get_config_value(lab + "_dir")) / box_name
		if sub_dir:
			cwd /= sub_dir


	init_session(box_name=box_name, box_dir=cwd, vpn_path=vpn_path,
		lab_name=lab, target=target, lhost=lhost, lport=lport)

	_create_cwd_if_not_exists(cwd, empty)
	_setup_tmux(cwd, vpn_path)
	_attach_to_tmux(cwd)

def _create_cwd_if_not_exists(cwd: Path, shall_be_empty: bool) -> None:
	if not os.path.exists(cwd):
		os.makedirs(cwd)

		if not shall_be_empty:
			for folder in get_config_value("default_folders"):
				os.mkdir(cwd / folder)


def _get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])


def _setup_tmux(cwd: Path, vpn_path: Path) -> None:
	os.system("tmux new-session -d -c {} -s Jarvis".format(cwd))
	os.system("tmux send -t Jarvis:0 'openvpn {}' C-m".format(vpn_path))
	time.sleep(0.1)
	os.system("tmux new-window -t Jarvis -c {}".format(cwd))

def _attach_to_tmux(cwd: Path) -> None:
	os.system("tmux at -t Jarvis -c {}".format(cwd))
