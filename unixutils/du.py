#http://stackoverflow.com/questions/4080254/python-os-stat-st-size-gives-different-value-than-du
#https://github.com/lunaryorn/snippets/blob/master/python-misc/du.py
import statvfs
import os 

st = os.statvfs("README.md") 

print "preferred block size", "=>", st[statvfs.F_BSIZE] / 1024
print "fundamental block size", "=>", st[statvfs.F_FRSIZE] / 1024
print "total blocks", "=>", st[statvfs.F_BLOCKS] / 1024
print "total free blocks", "=>", st[statvfs.F_BFREE] / 1024
print "available blocks", "=>", st[statvfs.F_BAVAIL] / 1024
print "total file nodes", "=>", st[statvfs.F_FILES] / 1024
print "total free nodes", "=>", st[statvfs.F_FFREE] / 1024
print "available nodes", "=>", st[statvfs.F_FAVAIL] / 1024
print "max file name length", "=>", st[statvfs.F_NAMEMAX] / 1024
