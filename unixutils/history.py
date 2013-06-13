import os
histfile = os.path.join(os.path.expanduser("~"), ".bash_history")
try:
    with open(histfile) as f:
        for l in enumerate(f.readlines()):
            print "  %s %s" % (l[0], l[1].rstrip('\n'))
except IOError:
    pass
