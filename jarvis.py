#!/usr/bin/python3

import os
import sys
import argparse
import importlib
from pathlib import Path


def get_script_path():
    return Path(os.path.dirname(os.path.realpath(sys.argv[0])))

_MODULE_DICT = {}
parser = argparse.ArgumentParser()
sub_parsers = parser.add_subparsers(dest="subcommand")

# import modules and link parsers
modules_path = get_script_path() / "modules"
print(modules_path)
for module_file in os.listdir(modules_path):
	if ".py" not in module_file:
		continue
	module_name = module_file.split(".")[0]
	module = importlib.import_module(f"modules.{module_name}", package=modules_path)
	module.add_parser(sub_parsers)
	_MODULE_DICT[module_name] = module.main


subcommand_args = dict(vars(parser.parse_args()))
subcommand = subcommand_args.pop("subcommand", None)

if not subcommand:
	parser.print_help()
	exit(1)

_MODULE_DICT[subcommand](**subcommand_args)
