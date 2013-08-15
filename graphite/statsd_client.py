#!/usr/bin/env python

usage = """
     Takes two arguments: <statsd ip> <statsd port>
        """

import socket
import time
import json
import sys

class StatsdClient(object):

        def __init__(self, ip, port):
            self.ip = ip
            self.port = int(port)

        def _send(self, msg, transport='udp'):

            if transport == 'tcp':
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
            s.connect((self.ip, self.port))
            try:
                s.sendall(msg)
                if transport == 'tcp':
                    return self.recv_basic(s)
                else:
                    return
            finally:
                s.close()

        def set(self, gauge, value):
            self._publish(gauge, value, 's')

        def timer(self, gauge, value):
            self._publish(gauge, value, 't')

        def gauge(self, gauge, value):
            self._publish(gauge, value, 'g')

        def increment(self, gauge, value):
            self._publish(gauge, value, 'c')

        def decrement(self, gauge, value):
            self._publish(gauge, '-' + value, 'c')

        def _publish(self, metric, value, type):
            #valid: metric:value|type
            statstring = metric +  ':' + str(value) + '|' + type
            return self._send(statstring)


def main():
    if len(sys.argv) < 3:
        print usage
        sys.exit(1)

    statengine = StatsdClient(sys.argv[1], sys.argv[2])
    statengine.gauge("blah", 1)
    statengine.set("hi", 1)

main()
