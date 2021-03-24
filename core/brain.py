import os
import tempfile
import json
from argparse import ArgumentParser
from pathlib import Path
from typing import Union


_BRAIN_FILE = Path(tempfile.gettempdir()) / ".jarvis.brain"
_SESSION_DATA = {}

if _BRAIN_FILE.is_file():
	with open(_BRAIN_FILE, "r") as brain_file:
		try:
			_SESSION_DATA = json.load(brain_file)
		except:
			_BRAIN_FILE.unlink() # invalid file format


def add_parser(sub_parsers: ArgumentParser) -> None:
	brain_parser = sub_parsers.add_parser("brain")
	brain_parser.add_argument("key", help="Brain Attribute", nargs="?", choices=["lhost", "lport", "target"], default=None)
	brain_parser.add_argument("value", help="Value for the attribute", nargs="?", default=None)

def main(key: str=None, value: str=None) -> None:
	if get_brain_value("active"):
		if not key and not value:
			for key in _SESSION_DATA.keys():
				print(f"{key}: {_SESSION_DATA[key]}")

		elif key and not value:
			print(f"Please specify a value for '{key}'")
			exit(0)

		elif key and value:
			set_brain_value(key, value)

	else:
		print("There is currently no active session!")

def init_session(box_dir, box_name, vpn_path, lab_name, target=None, lhost=None, lport=None):
	if get_brain_value("active"):
		print("A session is already active! Please exit it first before creating a new one!")
		exit(1)

	set_brain_value("active", True)
	set_brain_value("box_dir", str(box_dir))
	set_brain_value("box_name", box_name)
	set_brain_value("vpn_path", str(vpn_path))
	set_brain_value("lab_name", lab_name)
	set_brain_value("target", target)
	set_brain_value("lhost", lhost)
	set_brain_value("lport", lport)


def exit_session() -> None:
	if not get_brain_value("active"):
		print("There is currently no active session!")
		exit(1)

	if _BRAIN_FILE.is_file():
		_BRAIN_FILE.unlink()


def set_brain_value(key: str, value) -> None:
	_SESSION_DATA[key] = value
	_save()

	if key == "target":
		os.environ["target"] = value or ""
	elif key == "box_dir":
		os.environ["boxdir"] = value or ""

def get_brain_value(key: str) -> Union[str, None]:
		try:
			return _SESSION_DATA[key]
		except KeyError:
			return None

def _save() -> None:
	with open(_BRAIN_FILE, "w") as brain_file:
		json.dump(_SESSION_DATA, brain_file, indent=4)
