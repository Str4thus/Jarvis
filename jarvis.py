#!/usr/bin/python3
# Examples:
#
# jarvis htb blue
# jarvis htb laboratory --release
# jarvis thm adventofcyber2 --subdir day4

import argparse
from modules import join
from modules import config

parser = argparse.ArgumentParser()
sub_parsers = parser.add_subparsers(dest="subcommand")

join_parser = join.get_parser(sub_parsers)
config_parser = config.get_parser(sub_parsers)


args = parser.parse_args()

if not args.subcommand:
	parser.print_help()
	exit()

command_dict = {
	"join": lambda : join.join(args.kind, args.box_name, args.release, args.sub_dir),
	"config": lambda: config.config(args.key, args.value),
}

command_dict[args.subcommand]()
