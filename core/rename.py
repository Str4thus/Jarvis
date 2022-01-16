import os
from pathlib import Path
from modules.pwnbooks import pwnbooks_rename
from .brain import set_brain_value, get_brain_value
from .config import get_config_value
from .join import _create_cwd_if_not_exists


def add_parser(sub_parsers) -> None:
    rename_parser = sub_parsers.add_parser("rename")
    rename_parser.add_argument("new_box_name", help="Name of the new box/working directory")


def main(new_box_name: str) -> None:
    lab_name = get_brain_value("lab_name")
    cwd = Path(get_brain_value("box_dir"))
    current_box_name = get_brain_value("box_name")
    

    new_cwd = cwd.rename(Path(get_config_value(lab_name + "_dir")) / new_box_name)

    set_brain_value("box_dir", str(new_cwd))
    set_brain_value("box_name", new_box_name)

    pwnbooks_rename(lab_name, current_box_name, new_box_name)