import os
from pathlib import Path
from core.config import get_config_value


def pwnbooks_init(lab_name:str , box_name:str , template: str="ctf") -> None:
	pwnbooks_script = Path(get_config_value("pwnbooks_path")) / "pwnbooks.py"
	os.system(f"{pwnbooks_script} init {lab_name} {box_name} --template {template}")

def pwnbooks_rename(lab_name: str, current_box_name:str, new_box_name: str) -> None:
	pwnbooks_script = Path(get_config_value("pwnbooks_path")) / "pwnbooks.py"
	os.system(f"{pwnbooks_script} rename {lab_name} {current_box_name} {new_box_name}")