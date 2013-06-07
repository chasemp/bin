#!/usr/bin/env python
import sys
with open(sys.argv[1]) as f:
    for l in reversed(f.readlines()):
        sys.stdout.write(l)
