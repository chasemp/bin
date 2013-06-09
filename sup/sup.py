#!/usr/bin/env python
import argparse
import sys
import httplib
import datetime
import subprocess
import time
import socket
import json
import inspect
from ping import Ping
try:
    import Tkinter, tkMessageBox
    gui = True
except ImportError:
    gui = False
    pass

def popup(msg):
    root = Tkinter.Tk()
    root.withdraw()
    tkMessageBox.showinfo(sys.argv[0], str(msg))

def runBash(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = p.stdout.read().strip()
    return out

def broadcast_msg(msg):
    runBash('echo "%s" | wall' % str(msg))


class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


class supped(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.v = False
        self.vv = False

    def run(self):
        with Timer() as t:
            result = self.poll()
        #millis = int(round(t.interval * 1000))
        #print millis
        return result, '%.05f' % t.interval

    def poll(self):
        raise NotImplementedError("Subclasses should implement this!")


class sup_http(supped):

    def poll(self):
        self.port = self.port if self.port else 80
        try:
            conn = httplib.HTTPConnection(self.ip, self.port)
            conn.request("HEAD", "/")
            request_result = conn.getresponse()
            if request_result:
                status = '%s %s' % (request_result.status, request_result.reason)
            else:
                status = 'unavailable'
            if self.vv:
                self.vv_out = ''
                self.vv_out += 'Connection details:'
                for k, v in vars(request_result).iteritems():
                    if k != 'msg':
                        self.vv_out += '         %s %s\n' % (k, v)
                    else:
                        self.vv_out += 'Message details:\n'
                        for output in str(v).splitlines():
                            self.v_out += '        %s\n' % output
            return status
        except socket.error:
            return None

class sup_smtp(supped):

    def poll(self):
        self.port = self.port if self.port else 25
        import socket
        try:
            mark = 'ESMTP'
            sock = socket.socket()
            sock.connect((self.ip, self.port))
            data = sock.recv(2048)
            if mark in data:
                status = 'ok'
            else:
                status = 'failed'
            return status
        except socket.error:
            return None
        finally:
            sock.close()

class sup_redis(supped):

    def poll(self):
        import telnetlib
        self.port = self.port if self.port else 6379
        mark = 'PONG'
        try:
            tn = telnetlib.Telnet(self.ip, self.port)
            tn.read_very_eager()
            tn.write("PING\r\n")
            tn.write("info\r\n")
            tn.write("QUIT\r\n")  # this is where i enter my username
            data = tn.read_all()
            if mark in data:
                status = mark
            else:
                status = 'failed'
            return status
        except socket.error:
            return None

class sup_tcping(supped):

    def poll(self):
        self.port = self.port if self.port else 22
        import socket
        try:
            sock = socket.socket()
            sock.connect((self.ip, self.port))
            if isinstance(sock, socket._socketobject):
                status = 'ok'
            else:
                status = 'failed'
            return status
        except socket.error:
            return None
        finally:
            sock.close()



class sup_ping(supped):

    def poll(self):
        import socket
        try:
            p = Ping(self.ip, 1, 55)
            return p.do()
        except socket.error:
            print 'need superuser priviledges'
            
class sup_tcping(supped):

    def poll(self):
        self.port = self.port if self.port else 22
        import socket
        try:
            sock = socket.socket()
            sock.connect((self.ip, self.port))
            if isinstance(sock, socket._socketobject):
                status = 'ok'
            else:
                status = 'failed'
            return status
        except socket.error:
            return None
        finally:
            sock.close()

def find_monitors(module):
    import sys
    sup_functions = {}
    classes = inspect.getmembers(module, inspect.isclass)
    for name, obj in classes:
        sup_functions[name] = obj
    return sup_functions

def main():

    sup_dict = find_monitors(sys.modules[__name__])
    parser = argparse.ArgumentParser(description='like ping but for protocols')
    parser.add_argument("site",nargs=1, help='url or ip of site to manage')
    parser.add_argument("-p", help="show popups",  action="store_true")
    parser.add_argument("-b", help="broadcast messages",  action="store_true")
    parser.add_argument("-v", help="verbose",  action="store_true")
    parser.add_argument("-vv", help="very verbose",  action="store_true")
    parser.add_argument("-t", help="use tcp only",  action="store_true")
    parser.add_argument('-s', action='store', dest='seconds',
                    default=2,
                    help='seconds between polls',
                    )

    parser.add_argument('-m', action='store', dest='mode',
                    default='tcping',
                    help='check type to use',
                    )

    def helpdie(msg=None):
        if msg:
            print '\n\nFailed: %s\n' % msg
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    site = args.site[0]

    if ':' in site:
        site, port = site.split(':')
        try:
            port = int(port)
        except ValueError, e:
            helpdie(str(e))
    else:
        port = 0

    if args.seconds:
        try:
            seconds = int(args.seconds)
        except Exception, e:
            helpdie(str(e))

    try:
        ip = socket.gethostbyname(site)
    except:
        helpdie('could not translate hostname')

    if gui == False and args.p:
        print 'popups enabled but no GUI -- disabling'
        args.p = False

    if args.vv:
        print args

    attempt = 0
    status = ''
    mode = "sup_%s" % args.mode
    if mode in sup_dict:
        suping = sup_dict[mode]
        s = suping(site, port)
        s.name = mode
        s.v = args.v
        s.vv = args.vv
    else:
        helpdie()

    if args.v or args.vv:
        print "Looking for %s on %s" % (mode, s.port)
    while 1:
        attempt += 1
        now = datetime.datetime.now()
        lstatus = status or ''
        status = s.run()
        if args.vv:
            print s.v_out
            sys.stdout.write('>>> ')

        host = s.ip
        if s.port:
            host += ':%s' % s.port
        msg = '%s %s %s %s' %  (now, host, status, attempt)

        if status and lstatus and status != lstatus:
            if args.b:
                broadcast_msg(msg)
            if args.p:
                popup(msg)
        elif status and not lstatus:
            if args.v:
                print 'unknown last state'

        print msg
        if args.v or args.vv:
            print '---------------------------------------------------'
        time.sleep(seconds)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\n'
        sys.exit(0)
