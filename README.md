# Jarvis


## Core Modules

### brain
Stores session relevant data upon `join`ing. [WIP]

---

### config
> `pwnbooks.py config <key> <value>`

Allows configuration of certain values, used by `jarvis.py`.

| Key     | Type | Description  | Example |
|:-------:|:----:| -----:| -----:|
| pwnbooks_path | Path | Path to the `pwnbooks.py` script (Optional) | /root/pwnbooks |
| default_folders | List | List of default folders, that should be present upon joining a new box | nmap,gobust,vhost |
| <lab_name>_dir | Path | Working directory upon joining a box. Subsitute <lab_name> with the desired lab | /ctf/htb/boxes |
| <lab_name>_vpn | Path | Path to the VPN file for the desired lab. | /ctf/htb/str4thus.ovpn |
| configured_labs | List | **SHOULD NOT BE MANIPULATED MANUALLY** List of all configured labs | htb,thm,endgame |

---

### exit
> `jarvis.py exit`

Allows quitting the current `jarvis.py` session and allowing to hop into a new one. This command can only be used in a valid session.

---

### join
> `jarvis.py join <lab_name> <box_name>`

Automates the CTF setup process such as setting up directories, creating a TMUX session and establishing VPN connection.

Example: `jarvis.py join htb blue --release --target 10.10.10.14 --pwnbooks`
- creates a folder called `blue` under `htb_dir`
- connects to the htb `release` vpn (`htb_release_vpn`, HTB only)
- starts a TMUX session
- sets the `target` IP to `10.10.10.14`, which is available via `$target` in the terminal
- initializes notes using `pwnbooks.py`

---

### labs
> `jarvis.py labs add <lab_name> --dir <lab_dir> --vpn <lab_vpn>`
> `jarvis.py labs remove <lab_name>`

Manages lab directories and VPNs. All registered labs can be found in `.jarvis.conf` under `configured_labs` and all lab directories / lab VPNs can be configured via `jarvis.py config`

## Extensions

### nmap
> `jarvis.py nmap <mode>`

Wrapper around `nmap` to make it easier and cleaner for default scans, as it automatically logs the output in the `nmap` directory of each lab.

Currently supported modes:
- `default`
- `fast`
- `udp`

---

### gobuster
> `jarvis.py gobust <wordlist_size>`

Wrapper around `gobuster` to make it easier and cleaner for default gobusts, as it automatically logs the output in the `gobust` directory of each lab. The `target` defaults to the one specifed upon joining. 

It uses the seclists `raft-<size>-words.txt` as wordlist, depending on the size.

Currently supported sizes:
- `small`
- `medium`
- `large`
---

### vhost
> `jarvis.py vhost <wordlist_size> <domain>`

Wrapper around gobusters `vhost` mode to make it easier and cleaner for default subdomain enumeration, as it automatically logs the output in the `vhost` directory of each lab.

Currently supported sizes:
- `small`
- `medium`
- `large`
---

### pwnbooks
Internal `pwnbooks.py` integration. Does not have direct user interaction. [WIP]