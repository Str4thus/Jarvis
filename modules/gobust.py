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
jarvis.py gobust dir seclists large /api/v2/users --backups
jarvis.py gobust vhost medium blue.htb
