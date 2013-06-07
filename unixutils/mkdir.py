import os
import sys
mode = 'p' if '-p' in sys.argv else 'n'
if mode == 'p':
    pi = sys.argv.index('-p')
    del sys.argv[pi]
    sys.argv.pop(0)
    if len(sys.argv) > 1:
        print 'unknown arguments'
    else:
        os.makedirs(sys.argv[0])
    sys.exit(0)
os.mkdir(sys.argv[1])
