from .config import get_config_value, set_config_value, remove_config_value
from argparse import ArgumentParser
from typing import List

def add_parser(sub_parsers: ArgumentParser) -> None:
	labs_parser = sub_parsers.add_parser("labs")
	labs_parser.add_argument("action", help="What action should be performed on the lab", choices=["add", "remove"])
	labs_parser.add_argument("name", help="Name of the lab")
	labs_parser.add_argument("--dir", help="Root directory of the lab", dest="lab_dir", default=None)
	labs_parser.add_argument("--vpn", help="Path to the vpn for the lab", dest="lab_vpn", default=None)

def main(action: str, name: str, lab_dir: str=None, lab_vpn: str=None) -> None:
	if action == "add":
		_add_lab(name, lab_dir, lab_vpn)
	elif action == "remove":
		_remove_lab(name)


def _add_lab(name: str, lab_dir: str=None, lab_vpn: str=None ) -> None:
	configured_labs = get_config_value("configured_labs") or []
	if name in configured_labs:
		print(f"'{name}' is already configured!")
		exit(1)

	lab_dir = lab_dir if lab_dir else input("Root directory of the lab: ")
	lab_vpn = lab_vpn if lab_vpn else input("Path to the lab vpn: ")
	set_config_value(f"{name}_dir", lab_dir)
	set_config_value(f"{name}_vpn", lab_vpn)

	configured_labs.append(name)
	set_config_value("configured_labs", configured_labs)

def _remove_lab(name: str) -> None:
	configured_labs = get_config_value("configured_labs") or []

	if name not in configured_labs:
		print(f"'{name}' is not configured!")
		exit(1)

	if not remove_config_value(f"{name}_dir"):
		print("Could not find the root directory for the lab!")
	if not remove_config_value(f"{name}_vpn"):
		print("Could not find the vpn path for the lab!")

	configured_labs.remove(name)
	configured_labs = configured_labs if len(configured_labs) > 0 else []
	set_config_value("configured_labs", configured_labs)
