import argparse
import sys
#conforms to: http://en.wikipedia.org/wiki/Cut_(Unix)
parser = argparse.ArgumentParser(description='blogging from cli')
parser.add_argument('-b', action="store", dest="bytes", help='bytes to retrieve')
parser.add_argument('-c', action="store", dest="chars", help='range of characters to return')
parser.add_argument('-d', action="store", dest="delim", help='delimiter')
parser.add_argument('-f', action="store", dest="fieldl", help='field list')
parser.add_argument('cfile', nargs='+')
args = parser.parse_args()

if args.bytes:
    with open(args.cfile[0], 'rb') as f:
        byte_s = f.read(int(args.bytes[0]))
        print byte_s

if args.chars:
    start, finish = args.chars.split('-')
    start = int(start) - 1
    finish = int(finish)
    with open(args.cfile[0], 'rb') as f:
        lines = f.readlines()
    for l in lines:
        stripfinish = l[:finish]
        print stripfinish[start:] 

if args.delim:
    delim = args.delim
    through = False
    if '-' in args.fieldl:
        if args.fieldl[-1] == '-':
            through = True
        if args.fieldl[0].isdigit():
            field = args.fieldl[0]
        else:
            print 'usage'
            sys.exit(1)
    else:
        field = args.fieldl

    field = int(field) - 1
    with open(args.cfile[0], 'rb') as f:
        lines = f.readlines()
    for l in lines:
        if delim in l:
            breakup = l.rstrip('\n').split(delim)
            if through:
                print delim.join(breakup[field:])
            else:
                print breakup[field]
        else:
            print l
