import os
import time
from pathlib import Path
from .config import get_config_value
from argparse import ArgumentParser


def add_parser(sub_parsers: ArgumentParser) -> None:
	join_parser = sub_parsers.add_parser("join")
	join_parser.add_argument("kind", help="Kind of CTF", choices=["htb", "thm"])
	join_parser.add_argument("box_name", help="Name of the box/working directory")
	join_parser.add_argument("--release", help="Connects to the release arena on HTB", action="store_true", default=False)
	join_parser.add_argument("--subdir", help="Subdirectory to create within the working directory (useful when a CTF consists of couple daily challenges)", dest="sub_dir", default=None)
	join_parser.add_argument("--empty", help="Do not create default folders inside (nmap, gobuster, etc)", action="store_true", default=False)
	join_parser.add_argument("--vpn", help="Specify a VPN to use", dest="vpn_path", default=None)


def main(kind: str, box_name: str, release: bool=False, empty: bool=False, sub_dir: str=None, vpn_path: str=None) -> None:
	if kind == "thm" and release:
		print("WARNING: recheck --release flag. Connecting to THM")

	if not vpn_path:
		if release:
			vpn_path = Path(get_config_value(kind + "_release_vpn"))
		else:
			vpn_path = Path(get_config_value(kind + "_vpn"))

	cwd = Path(get_config_value(kind + "_dir")) / box_name
	if sub_dir:
		cwd /= sub_dir


	_create_cwd_if_not_exist(cwd, empty)
	_setup_tmux(cwd, vpn_path)


def _create_cwd_if_not_exist(cwd: Path, shall_be_empty: bool) -> None:
	if not os.path.exists(cwd):
		os.makedirs(cwd)

		if not shall_be_empty:
			for folder in get_config_value("default_folders"):
				os.mkdir(cwd / folder)


def _setup_tmux(cwd: Path, vpn_path: Path) -> None:
	os.system("tmux new-session -d -c {} -s Jarvis".format(cwd))
	os.system("tmux new-window -t Jarvis -c {}".format(cwd))
	os.system("tmux send -t Jarvis:0 'openvpn {}' C-m".format(vpn_path))
	os.system("tmux at -t Jarvis -c {}".format(cwd))
