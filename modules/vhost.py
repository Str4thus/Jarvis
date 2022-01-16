import os
import time
from pathlib import Path
from core.brain import get_brain_value

_WORDLIST_MAP= {
    "small": "subdomains-top1million-5000.txt",
    "medium": "subdomains-top1million-20000.txt",
    "large": "subdomains-top1million-110000.txt",
}


def add_parser(sub_parsers) -> None:
    vhost_parser = sub_parsers.add_parser("vhost")
    vhost_parser.add_argument("wordlist_size", help="Size of the wordlist (uses subdomains-top1million-xxx.txt)", choices=["small", "medium", "large"])
    vhost_parser.add_argument("domain", help="Domain to brute vhost on")
    vhost_parser.add_argument("-p", "--port", help="Specifies a port (default is 80)", dest="port", type=int, default=80)
    vhost_parser.add_argument("--ssl", help="Use https instead of http", action="store_true", dest="use_ssl", default=False)
	
    default_vhost_dir = str(Path(get_brain_value("box_dir")) / "vhost") if get_brain_value("box_dir") else None
    vhost_parser.add_argument("-o --output", help="Output directory (default is ./vhost)", dest="output_dir", default=default_vhost_dir)


def main(wordlist_size: str, domain: str, port: int=80, use_ssl: bool=False, output_dir: str=None, unknown_args: str="") -> None:
    protocol = "https" if use_ssl else "http"
    full_url = f"{protocol}://{domain}:{port}"

    output_dir_flag = ""

    if os.path.isdir(output_dir):
        output_dir_flag = f"-o {output_dir}/{domain}.ffuf"
    else:
        print(f"WARNING: Jarvis won't log this vhost scan. Please create {output_dir} to fix this.")
        time.sleep(3)
  
    os.system(f"ffuf -u {full_url} -w /usr/share/seclists/Discovery/DNS/{_map_size_to_wordlist(wordlist_size)} -H 'Host: FUZZ.{domain}' -mc all {output_dir_flag} {unknown_args}")


def _map_size_to_wordlist(wordlist_size):
    return _WORDLIST_MAP[wordlist_size]