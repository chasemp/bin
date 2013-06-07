#Specify by name only atm
from os import stat
import sys
import pwd
import grp
import os

if len(sys.argv) < 2:
    print 'wtf'
group = sys.argv[1]
file = sys.argv[-1]
if file == sys.argv[1]:
    print 'please specify a file'
    sys.exit(0)

try:
    gid = grp.getgrnam(group).gr_gid
except KeyError:
    print 'could not find grp: ' + group
    sys.exit(1)

#Get current user as os.chown wants both params
uid = stat(file).st_uid
os.chown(file, uid, gid)
