import os
import time
from .brain import exit_session
from argparse import ArgumentParser

def add_parser(sub_parsers: ArgumentParser) -> None:
	exit_parser = sub_parsers.add_parser("exit")

def main():
	exit_session()
	os.system("tmux send -t Jarvis:0 C-c")
	time.sleep(0.1)
	os.system("tmux kill-session -t Jarvis")
