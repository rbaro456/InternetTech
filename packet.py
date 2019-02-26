import binascii
import socket as syssock
import struct
import sys


class Packet:

    def __init__(self, version, flags, header_len, sequence_no, ack_no, payload_len):
        self.version = version
        self.flags = flags
        self.opt_ptr = 0x0
        self.protocol = 0x0
        self.header_len = header_len
        self.checksum = 0x0
        self.source_port = 0x0
        self.dest_port = 0x0
        self.sequence_no = sequence_no
        self.ack_no = ack_no
        self.window = 0x0
        self.payload_len = payload_len

    def pack(self):
        sock352PktHdrData = '!BBBBHHLLQQLL'
        udpPkt_hdr_data = struct.Struct(sock352PktHdrData)
        header = udpPkt_hdr_data.pack(self.version, self.flags, self.opt_ptr, self.protocol, self.header_len,
                                      self.checksum, self.source_port, self.dest_port, self.sequence_no,
                                      self.ack_no, self.window, self.payload_len)
        print "printing header data"
        print header
        return header

    @staticmethod
    def unpack(bytes):
        data = struct.unpack('!BBBBHHLLQQLL', bytes)
        print "unpack data"
        packet = Packet(data[0], data[1], data[4], data[8], data[9], data[11])
        return packet

    @staticmethod
    def get_size_of_packet():
        size = struct.calcsize('!BBBBHHLLQQLL')
        print " Size of packet is "
        print size
        return size



