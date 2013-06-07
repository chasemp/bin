import sys
import os
path, trail = os.path.split(sys.argv[1])

if len(sys.argv) > 2:
   stripped = sys.argv[-1]
   print trail.rstrip(stripped)
   sys.exit(0)   
print trail
