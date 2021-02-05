import json
from argparse import ArgumentParser
from pathlib import Path



_CONFIG_FILE = Path.home() / ".jarvis.conf"

_DEFAULT_CONFIG = {
	"htb_vpn": "", # Path to HTB vpn
	"thm_vpn": "", # Path to THM vpn
	"htb_dir": "", # Path to HTB root dir
	"thm_dir": "", # Path to THM root dir
	"default_folders": ["nmap", "gobuster"], # Default folders for initialization
}

if not _CONFIG_FILE.is_file():
	with open(_CONFIG_FILE, "w") as config_file:
		json.dump(_DEFAULT_CONFIG, config_file, indent=4)


with open(_CONFIG_FILE, "r") as config_file:
	_CONFIG = json.load(config_file)



def get_parser(sub_parsers: ArgumentParser) -> ArgumentParser:
	config_parser = sub_parsers.add_parser("config")
	config_parser.add_argument("key", help="Configuration key", choices=_CONFIG.keys())
	config_parser.add_argument("value", help="Value for the key")
	return config_parser

def config(key: str, value: str) -> None:
	if "," in value:
		_CONFIG[key] = value.split(",")
	else:
		_CONFIG[key] = value
	_save_config()


def _save_config() -> None:
	with open(_CONFIG_FILE, "w") as config_file:
		json.dump(_CONFIG, config_file, indent=4)

def get_config_value(key: str) -> str:
	return _CONFIG[key]
