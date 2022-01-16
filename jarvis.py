#!/usr/bin/python3

# Should be added to ~/.bashrc
# alias target="echo Y2F0IC90bXAvLmphcnZpcy5icmFpbiB8IGdyZXAgInRhcmdldCIgfCBhd2sgLUY6ICd7Z3N1YigvIi8sICIiKTsgZ3N1YigvIC8sICIiKTsgcHJpbnQgJDJ9Jw== | base64 -d | sh"

import os
import sys
import argparse
import importlib
from pathlib import Path


_MODULE_DICT = {}
parser = argparse.ArgumentParser()
sub_parsers = parser.add_subparsers(dest="subcommand")


def get_script_path():
    return Path(os.path.dirname(os.path.realpath(sys.argv[0])))

def import_modules(folder: str):
	module_dir = get_script_path() / folder
	for module_file in os.listdir(module_dir):
		if ".py" not in module_file:
			continue

		module_name = module_file.split(".")[0]
		module = importlib.import_module(f"{folder}.{module_name}")
		
		try:
			module.add_parser(sub_parsers)
			_MODULE_DICT[module_name] = module.main
		except:
			pass
		


if __name__ == "__main__":
	# import modules and link parsers
	import_modules("core")
	import_modules("modules")

	subcommand_args, unknown_args = parser.parse_known_args()
	unknown_args = " ".join(unknown_args)

	subcommand_args = dict(vars(subcommand_args))

	if unknown_args:
		subcommand_args["unknown_args"] = unknown_args

	subcommand = subcommand_args.pop("subcommand", None)

	if not subcommand:
		parser.print_help()
		exit(1)
	
	#try:
	_MODULE_DICT[subcommand](**subcommand_args)
	#except TypeError:
	#	print(f"Module '{subcommand}' does not accept additional arguments!")
