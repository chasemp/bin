import socket

# addressing information of target
IPADDR = '127.0.0.1'
PORTNUM = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.connect((IPADDR, PORTNUM))
total = ''
s.send("goodcount:1|c|@0.5")
s.send("goodcount:1|c|@1")
s.send("badcount1:2|c|@")
s.send("badcount2:3|c|what")
s.send("notype:5|")
s.send("no|:5g")
s.close()
