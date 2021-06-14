import os
from pathlib import Path
from core.config import get_config_value


def pwnbooks_init(lab_name:str , box_name:str , template: str="ctf"):
	pwnbooks_script = Path(get_config_value("pwnbooks_path")) / "pwnbooks.py"
	os.system(f"{pwnbooks_script} init {lab_name} {box_name} --template {template}")