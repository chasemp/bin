#!/usr/bin/env python

import argparse
import socket
import time
from random import randint

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 8000

def send(m):
    sock = socket.socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(m)
    sock.close()

while 1:
    print 'send', time.time()
    send('test.yup:1|s')
    time.sleep(10)
