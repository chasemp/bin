#!/usr/bin/env python
import sys
import argparse
parser = argparse.ArgumentParser(description='blogging from cli')
parser.add_argument('-n', action="store", dest="lines", help='number of lines to return', default='3')
parser.add_argument("file", nargs="+")
args = parser.parse_args()
assert args.file
with open(args.file[-1]) as f:
    lines = f.readlines()
    for i in range(0, int(args.lines)):
        sys.stdout.write(lines[i])
