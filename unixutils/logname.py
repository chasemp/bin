import getpass
import os
try:
    user = os.getenv('SUDO_USER')
except:
    if os.geteuid() == 0:
        user = "root"
    else:
        user = getpass.getuser()

print user
