from pathlib import Path
from modules.pwnbooks import pwnbooks_init
from .brain import set_brain_value, get_brain_value
from .config import get_config_value
from .join import _create_cwd_if_not_exists


def add_parser(sub_parsers) -> None:
    pivot_parser = sub_parsers.add_parser("pivot")
    pivot_parser.add_argument("new_box_name", help="Name of the new box/working directory")
    pivot_parser.add_argument("-t", "--target", help="Specify the target's ip", default=None)
    pivot_parser.add_argument("--pwnbooks", help="Generate notes for this box", dest="shall_init_pwnbooks", action="store_true", default=False)


def main(new_box_name: str, target: str=None, shall_init_pwnbooks: bool=False) -> None:
    lab_name = get_brain_value("lab_name")
    new_cwd = Path(get_config_value(lab_name + "_dir")) / new_box_name

    set_brain_value("box_dir", str(new_cwd))
    set_brain_value("target", target)
    set_brain_value("box_name", new_box_name)

    _create_cwd_if_not_exists(new_cwd)

    if shall_init_pwnbooks:
        pwnbooks_init(lab_name, new_box_name)