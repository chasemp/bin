#!/usr/bin/env python
import sys
import pydoc
with open(sys.argv[1], 'r') as f:
    pydoc.pager(f.read())
