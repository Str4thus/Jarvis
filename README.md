# Jarvis


## Base Modules

### config
Allows configuration of Jarvis

Example: `jarvis.py config thm_dir /root/thm`
- Sets the **base directory** for THM rooms to **/root/thm**

---

### join
Automates the CTF setup process (Directories, TMUX, VPN)

Example: `jarvis.py join htb blue --release`
- Creates a folder called **blue** in the diretory specified in the config and connects to the **htb release** vpn
- Starts a TMUX session

Possible Configurations:

| Key     | Type | Description  | Example |
|:-------:|:----:| -----:| -----:|
| htb_vpn | Path | Path to the .ovpn file for the HTB VPN | /root/htb/skid.ovpn |
| htb_release_vpn | Path | Path to the .ovpn file for the HTB VPN | /root/htb/skid-release.ovpn |
| thm_vpn | Path | Path to the .ovpn file for the THM VPN | /root/thm/skid.ovpn |
| htb_dir | Path | Path to the base directory of the HTB boxes | /root/htb/boxes |
| thm_dir | Path | Path to the base directory of the THM rooms | /root/thm/rooms |
| default_folders | List | List of the folders created upon initialization | nmap,gobuster,ssh |
| pwnbooks_path | Path | Path to the folder of the pwnbooks.py script | /tools/pwnbooks |
---

### nmap

---

### gobuster

---
