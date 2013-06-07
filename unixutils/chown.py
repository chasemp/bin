#Specify by name only atm
import sys
import pwd
import grp
import os

if len(sys.argv) < 2:
    print 'wtf'

if ':' in sys.argv[1]:
    user, group = sys.argv[1].split(':')

file = sys.argv[-1]
if file == sys.argv[1]:
    print 'please specify a file'
    sys.exit(0)

try:
    uid = pwd.getpwnam(user).pw_uid
except KeyError:
    print 'could not find user: ' + user
    sys.exit(1)
try:
    gid = grp.getgrnam(group).gr_gid
except KeyError:
    print 'could not find grp: ' + group
    sys.exit(1)

os.chown(file, uid, gid)
