import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Union, List

_CONFIG_FILE = Path.home() / ".jarvis.conf"

_DEFAULT_CONFIG = {
	"pwnbooks_path": "/pwnbooks", # Path to the pwnbooks package
	"default_folders": ["nmap", "gobuster"], # Default folders for initialization
	"configured_labs": []
}

if not _CONFIG_FILE.is_file():
	with open(_CONFIG_FILE, "w") as config_file:
		json.dump(_DEFAULT_CONFIG, config_file, indent=4)


with open(_CONFIG_FILE, "r") as config_file:
	_CONFIG = json.load(config_file)



def add_parser(sub_parsers: ArgumentParser) -> None:
	config_parser = sub_parsers.add_parser("config")
	config_parser.add_argument("key", help="Configuration key", choices=_CONFIG.keys())
	config_parser.add_argument("value", help="Value for the key")


def main(key: str, value: str, new_lab_name: str=None) -> None:
	if "," in value:
		set_config_value(key, value.split(","))
	else:
		set_config_value(key, value)


def get_config_value(key: str) -> Union[str, None]:
	try:
		return _CONFIG[key]
	except KeyError:
		return None

def set_config_value(key: str, value) -> None:
	_CONFIG[key] = value
	_save_config()

def remove_config_value(key) -> bool:
	try:
		del _CONFIG[key]
		_save_config()
		return True
	except KeyError:
		return False


def _save_config() -> None:
	with open(_CONFIG_FILE, "w") as config_file:
		json.dump(_CONFIG, config_file, indent=4)
