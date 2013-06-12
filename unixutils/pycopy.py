#pycopy to avoid bad 'copy' imports for various tools
import sys
import shutil

mode = 'p' if '-p' in sys.argv else None
mode = 'r' if '-r' in sys.argv else None

if mode == 'r': 
    print 'r'
    shutil.copytree(sys.argv[1], sys.argv[2], symlinks=False, ignore=None)
if mode == 'p': 
    print 'p'
    shutil.copy2(sys.argv[1], sys.argv[2])
else:
    shutil.copyfile(sys.argv[1], sys.argv[2])


