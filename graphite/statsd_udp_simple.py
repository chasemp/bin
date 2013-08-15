import socket
IPADDR = '127.0.0.1'
PORTNUM = 8125
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.connect((IPADDR, PORTNUM))
total = ''
for i in range(1, 10):
    s.send("testme%s:%d|g\ntestme2:5|g" % (str(i), i))
s.close()
