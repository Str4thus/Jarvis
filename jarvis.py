#!/usr/bin/python3

import os
import argparse
import importlib
from inspect import signature 

_MODULE_DICT = {}
parser = argparse.ArgumentParser()
sub_parsers = parser.add_subparsers(dest="subcommand")

# import modules and link parsers
for module_file in os.listdir("modules"):
	if ".py" not in module_file:
		continue
	module_name = module_file.split(".")[0]
	module = importlib.import_module("modules." + module_name)
	module.add_parser(sub_parsers)
	_MODULE_DICT[module_name] = module.main


subcommand_args = dict(vars(parser.parse_args()))
subcommand = subcommand_args.pop("subcommand", None)

if not subcommand:
	parser.print_help()
	exit()

_MODULE_DICT[subcommand](**subcommand_args)
