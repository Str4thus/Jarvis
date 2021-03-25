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
	
    default_vhost_dir = str(Path(get_brain_value("box_dir")) / "vhost") if get_brain_value("box_dir") else None
    vhost_parser.add_argument("-o --output", help="Output directory (default is ./vhost)", dest="output_dir", default=default_vhost_dir)


def main(wordlist_size: str, domain: str, output_dir: str=None) -> None:
    output_dir_flag = ""

    if os.path.isdir(output_dir):
        output_dir_flag = f"-o {output_dir}/{domain}.dns"
    else:
        print(f"WARNING: Jarvis won't log this vhost scan. Please create {output_dir} to fix this.")
        time.sleep(3)
  
    #os.system(f"wfuzz -c {output_dir_flag} -Z -w /usr/share/seclists/Discovery/DNS/{_map_size_to_wordlist(wordlist_size)} --sc 200,202,204,301,302,307,403 FUZZ.{domain}")
    os.system(f"gobuster vhost -u {domain} -w /usr/share/seclists/Discovery/DNS/{_map_size_to_wordlist(wordlist_size)} {output_dir_flag}")


def _map_size_to_wordlist(wordlist_size):
    return _WORDLIST_MAP[wordlist_size]