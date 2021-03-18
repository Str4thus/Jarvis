from .brain import exit_session
from argparse import ArgumentParser

def add_parser(sub_parsers: ArgumentParser) -> None:
	exit_parser = sub_parsers.add_parser("exit")

def main():
	# TODO: clean up tmux session and disconnect from vpn
	exit_session()
