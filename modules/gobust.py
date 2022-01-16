"""
jarvis.py gobust dir [dirb, seclists] [small,medium,large] <path> -p <port DEFAULT=80> [-x <ext>, --backups]
jarvis.py gobust vhost [small, medium, large] [domain]

# gobuster dir -u 'http://<target>:<port><path>' -w /usr/share/seclists/Discovery/Web-Content/raft-<?>-words.txt -o gobuster/<target>-<port>-<path>-[ext].gobust -x [ext]'
# gobuster vhost -u <domain> -w /usr/share/seclists/.. -o vhost-<domain but replace . with - >.gobust

Log Files:
- /api/v2/users-31337-10.10.104
- vhost-google-com.gobust

10.10.10.104-31337-/api/v2/users-ext.gobust

jarvis.py gobust dir dirb small php,ini
jarvis.py gobust dir dirb large /api/v2/users -p 1337 -x php,html,txt
jarvis.py gobust vhost medium blue.htb
"""

import os
import time
from core.brain import get_brain_value
from pathlib import Path

def add_parser(sub_parsers) -> None:
	gobust_parser = sub_parsers.add_parser("gobust")
	gobust_parser.add_argument("wordlist_size", help="Size of the wordlist (uses raft-<size>-words.txt)", choices=["small", "medium", "large"])
	gobust_parser.add_argument("-u", "--url", help="Path of the url (e.g. /home or /admin/dashboard)", dest="url_path", default="/")
	gobust_parser.add_argument("-x", "--extensions", help="Specify extensions to look for (format: ext1,ext2,ext3)", dest="extensions", type=str, default="")
	gobust_parser.add_argument("-t", "--target", help="Target IP (default is the active target, if configured)", dest="target_ip", default=get_brain_value("target"))
	gobust_parser.add_argument("-p", "--port", help="Specifies a port (default is 80)", dest="port", type=int, default=80)
	gobust_parser.add_argument("--ssl", help="Use https instead of http", action="store_true", dest="use_ssl", default=False)
	

	default_gobust_dir = str(Path(get_brain_value("box_dir")) / "gobuster") if get_brain_value("box_dir") else None
	gobust_parser.add_argument("-o --output", help="Output directory (default is ./gobust)", dest="output_dir", default=default_gobust_dir)


def main(wordlist_size: str, url_path: str="/", target_ip: str=None, port: int=80, 
		use_ssl: bool=False, extensions: str="", output_dir: str=None, unknown_args: str="") -> None:

	if unknown_args:
		print(f"Passing arguments '{unknown_args}' forward.")

	if not get_brain_value("active"):
		print("This module is only available in a valid session!")
		exit(1)

	if not target_ip:
		print("Please specify a target via the --target switch or via 'jarvis.py brain target <ip>''")
		exit(1)

	_gobust(url_path, wordlist_size, target_ip, port, use_ssl, extensions, output_dir, unknown_args)

def _gobust(url_path: str, wordlist_size: str, target_ip: str, port: int, use_ssl: bool, extensions: str, output_dir: str, unknown_args: str) -> None:
	if len(url_path) > 0 and url_path[0] != "/":
		url_path = "/" + url_path

	protocol = "https" if use_ssl else "http"
	full_url = f"{protocol}://{target_ip}:{port}{url_path}"

	extensions_flag = ""
	output_dir_flag = ""

	if len(extensions) > 0:
		extensions_flag = f"-x {extensions}" 
	
	if os.path.isdir(output_dir):
		output_dir_flag = f"-o {output_dir}/{port}{url_path.replace('/','-') if len(url_path) > 1 else '-root'}.gobust"
	else:
		print(f"WARNING: Jarvis won't log this gobust. Please create {output_dir} to fix this.")
		time.sleep(3)
	
	os.system(f"gobuster dir -u {full_url} -w /usr/share/seclists/Discovery/Web-Content/raft-{wordlist_size}-words.txt {extensions_flag} {output_dir_flag} {unknown_args}")
	
