import time
import sys
if len(sys.argv) < 2:
    print 'usage: sleep seconds'
    sys.exit(0)
interval = sys.argv[1]
try:
    interval = int(interval)
except:
    sys.exit(0)   
time.sleep(interval)
