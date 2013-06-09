#!/usr/bin/env python
# coding: utf-8

"""
    https://github.com/jedie/python-ping/blob/master/ping.py

    A pure python ping implementation using raw sockets.

    Note that ICMP messages can only be send from processes running as root
    (in Windows, you must run this script as 'Administrator').

    Bugs are naturally mine. I'd be glad to hear about them. There are
    certainly word - size dependencies here.
    
    :homepage: https://github.com/jedie/python-ping/
    :copyleft: 1989-2011 by the python-ping team, see AUTHORS for more details.
    :license: GNU GPL v2, see LICENSE for more details.
"""


import array
import os
import select
import signal
import socket
import struct
import sys
import time


if sys.platform.startswith("win32"):
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time


# ICMP parameters
ICMP_ECHOREPLY = 0 # Echo reply (per RFC792)
ICMP_ECHO = 8 # Echo request (per RFC792)
ICMP_MAX_RECV = 2048 # Max size of incoming buffer

MAX_SLEEP = 1000


def calculate_checksum(source_string):
    """
    A port of the functionality of in_cksum() from ping.c
    Ideally this would act on the string as a series of 16-bit ints (host
    packed), but this works.
    Network data is big-endian, hosts are typically little-endian
    """
    if len(source_string)%2:
        source_string += "\x00"
    converted = array.array("H", source_string)
    if sys.byteorder == "big":
        converted.byteswap()
    val = sum(converted)

    val &= 0xffffffff # Truncate val to 32 bits (a variance from ping.c, which
                      # uses signed ints, but overflow is unlikely in ping)

    val = (val >> 16) + (val & 0xffff)    # Add high 16 bits to low 16 bits
    val += (val >> 16)                    # Add carry from above (if any)
    answer = ~val & 0xffff                # Invert and truncate to 16 bits
    answer = socket.htons(answer)

    return answer


def is_valid_ip4_address(addr):
    parts = addr.split(".")
    if not len(parts) == 4:
        return False
    for part in parts:
        try:
            number = int(part)
        except ValueError:
            return False
        if number > 255:
            return False
    return True

def to_ip(addr):
    if is_valid_ip4_address(addr):
        return addr
    return socket.gethostbyname(addr)


class Ping(object):
    def __init__(self, dest_ip, timeout=1000, packet_size=55, own_id=None):
        self.dest_ip = dest_ip
        self.timeout = timeout
        self.packet_size = packet_size
        if own_id is None:
            self.own_id = os.getpid() & 0xFFFF
        else:
            self.own_id = own_id

        self.seq_number = 0
        self.send_count = 0
        self.receive_count = 0
        self.min_time = 999999999
        self.max_time = 0.0
        self.total_time = 0.0

    def print_success(self, delay, ip, packet_size, ip_header, icmp_header):
        if ip == self.dest_ip:
            from_info = ip
        else:
            from_info = "%s (%s)" % (self.dest_ip, ip)

        return ("%d bytes - ttl=%d time=%.1f ms" % (
            packet_size, ip_header["ttl"], delay)
        )

    def header2dict(self, names, struct_format, data):
        """ unpack the raw received IP and ICMP header informations to a dict """
        unpacked_data = struct.unpack(struct_format, data)
        return dict(zip(names, unpacked_data))

    #--------------------------------------------------------------------------

    def run(self, count=None, deadline=None):
        """
        send and receive pings in a loop. Stop if count or until deadline.
        """
        while True:
            delay = self.do()

            self.seq_number += 1
            if count and self.seq_number >= count:
                break
            if deadline and self.total_time >= deadline:
                break

            if delay == None:
                delay = 0

            # Pause for the remainder of the MAX_SLEEP period (if applicable)
            if (MAX_SLEEP > delay):
                time.sleep((MAX_SLEEP - delay) / 1000.0)

    def do(self):
        """
        Send one ICMP ECHO_REQUEST and receive the response until self.timeout
        """
        try: # One could use UDP here, but it's obscure
            current_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
        except socket.error, (errno, msg):
            if errno == 1:
                # Operation not permitted - Add more information to traceback
                etype, evalue, etb = sys.exc_info()
                evalue = etype(
                    "%s - Note that ICMP messages can only be send from processes running as root." % evalue
                )
                raise etype, evalue, etb
            raise # raise the original error

        send_time = self.send_one_ping(current_socket)
        if send_time == None:
            return
        self.send_count += 1

        receive_time, packet_size, ip, ip_header, icmp_header = self.receive_one_ping(current_socket)
        current_socket.close()

        if receive_time:
            self.receive_count += 1
            delay = (receive_time - send_time) * 1000.0
            self.total_time += delay
            if self.min_time > delay:
                self.min_time = delay
            if self.max_time < delay:
                self.max_time = delay

            return self.print_success(delay, ip, packet_size, ip_header, icmp_header)
        else:
            return "Request timed out."

    def send_one_ping(self, current_socket):
        """
        Send one ICMP ECHO_REQUEST
        """
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        checksum = 0

        # Make a dummy header with a 0 checksum.
        header = struct.pack(
            "!BBHHH", ICMP_ECHO, 0, checksum, self.own_id, self.seq_number
        )

        padBytes = []
        startVal = 0x42
        for i in range(startVal, startVal + (self.packet_size)):
            padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
        data = bytes(padBytes)

        # Calculate the checksum on the data and the dummy header.
        checksum = calculate_checksum(header + data) # Checksum is in network order

        # Now that we have the right checksum, we put that in. It's just easier
        # to make up a new header than to stuff it into the dummy.
        header = struct.pack(
            "!BBHHH", ICMP_ECHO, 0, checksum, self.own_id, self.seq_number
        )

        packet = header + data

        send_time = default_timer()

        try:
            current_socket.sendto(packet, (self.dest_ip, 1)) # Port number is irrelevant for ICMP
        except socket.error as e:
            print("General failure (%s)" % (e.args[1]))
            current_socket.close()
            return

        return send_time

    def receive_one_ping(self, current_socket):
        """
        Receive the ping from the socket. timeout = in ms
        """
        timeout = self.timeout / 1000.0

        while True: # Loop while waiting for packet or timeout
            select_start = default_timer()
            inputready, outputready, exceptready = select.select([current_socket], [], [], timeout)
            select_duration = (default_timer() - select_start)
            if inputready == []: # timeout
                return None, 0, 0, 0, 0

            receive_time = default_timer()

            packet_data, address = current_socket.recvfrom(ICMP_MAX_RECV)

            icmp_header = self.header2dict(
                names=[
                    "type", "code", "checksum",
                    "packet_id", "seq_number"
                ],
                struct_format="!BBHHH",
                data=packet_data[20:28]
            )

            if icmp_header["packet_id"] == self.own_id: # Our packet
                ip_header = self.header2dict(
                    names=[
                        "version", "type", "length",
                        "id", "flags", "ttl", "protocol",
                        "checksum", "src_ip", "dest_ip"
                    ],
                    struct_format="!BBHHHBBHII",
                    data=packet_data[:20]
                )
                packet_size = len(packet_data) - 28
                ip = socket.inet_ntoa(struct.pack("!I", ip_header["src_ip"]))
                # XXX: Why not ip = address[0] ???
                return receive_time, packet_size, ip, ip_header, icmp_header

            timeout = timeout - select_duration
            if timeout <= 0:
                return None, 0, 0, 0, 0

#s = sup_ping('10.0.0.1', 0)
#print s.poll()
