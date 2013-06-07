import sys
import hashlib

args = sys.argv
args.pop(0)
mode = 'check' if '-c' in args else 'hash'

def hash(file):
    m = hashlib.md5()
    m.update(file)
    return m.hexdigest()

if mode == 'check':
    with open(sys.argv[1]) as f:
        sums = f.readlines()
        failed = 0
        success = 0
        for f in sums:
            fhash, file = f.rstrip('\n').split('  ')
            if fhash == hash(file):
                success += 1
                print '%s: OK' % (file,)
            else:
                failed += 1
                print '%s: FAILED' % (file,)
        if failed:
            status = 'md5sum: WARNING: %s of %s computed checksum did NOT match'
            print status % (failed, success + failed)
else:
    for file in args:
        sum = hash(open(file).read())
        print "%s  %s" % (sum, file)
