jarvis.py pwn listen # defaults to  nc -lnvp <lport>



:linpeas # uploads linpeas to /tmp or /dev/shm and executes. Also downloads the output
:upload <file> <rpath> # uploads a file to the server into the remote path
:download <file> <lpath> # downloads a file from the server into the local path
:upgrade # python -c 'import pty;pty.spawn("/bin/bash")', also try python3, export TERM=xterm



# When shell connects:
root@host# :linpeas
