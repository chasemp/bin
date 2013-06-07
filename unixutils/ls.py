#!/usr/bin/env python
import os
import sys
dir = '.' if len(sys.argv) < 2 else sys.argv[1]
files = os.listdir(dir)
for f in files:
    print f
