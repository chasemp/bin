#!/usr/bin/env python

import pickle
import time
import struct
import socket

list = [('chase', (time.time(), 1)), ('chase2', (time.time(), 1))]

print list
payload = pickle.dumps(list)
header = struct.pack("!L", len(payload))
message = header + payload

def main():
        s = socket.socket()
        s.connect(('10.1.107.27', 2003))
        s.sendall(message)
        s.close()
main()
