
import binascii
import socket as syssock
import struct
import sys
import random
import time

import packet

# Size of packets
PACKETSIZE = packet.Packet.get_size_of_packet()

# Different flags
SYN = 0x01
FIN = 0x02
ACK = 0x04
RESET = 0x08
HAS_OPT = 0xA0

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

global transmit_port

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here
    global transmit_port, receive_port
    transmit_port = UDPportTx
    receive_port = UDPportRx

class socket:

    def __init__(self):  # fill in your code here
        self.mySocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
        self.connect_address = None  # Address socket is connecting to
        self.curr_ack = 0
        self.curr_seq = 0
       # self.mySocket.settimeout(2)
        return

    def bind(self,address):
        print "Printin meow addy"
        print address
        self.mySocket.bind(address)
        return

    def connect(self,address):  # fill in your code here
        print "In the connect function...."
        print transmit_port

        sequence_no = random.randint(1, 500)


        connectPacket = packet.Packet(0x1, SYN, 0x0, sequence_no, 0x0, 0x0)  # Creating packet to send
        binaryData = connectPacket.pack()  # Pack into binary data

        self.curr_ack = 0x1 # Update to current ack number
        self.curr_seq = sequence_no  # Update to current ack number

        self.mySocket.sendto(binaryData, address)  # Send data to server

        binary, address = self.mySocket.recvfrom(PACKETSIZE)  # Wait for servers response

        self.connect_address = address  # Hold on to connection address

        server_packet = packet.Packet.unpack(binary)  # Unpack received packet

        print "Server packet info"
        print server_packet.version
        print server_packet.flags
        print server_packet.opt_ptr
        print server_packet.protocol
        print server_packet.header_len
        print server_packet.checksum
        print server_packet.source_port
        print server_packet.dest_port
        print server_packet.sequence_no
        print server_packet.ack_no
        print server_packet.window
        print server_packet.payload_len


        return

    def listen(self, backlog):
        #mySocket.listen(backlog)
        return

    def accept(self):
        print "Waiting for datakhgkug"

        # NEED TO ALSO CHECK IF SERVER IS CONNECTED TO ANOTHER CLIENT!!!!!!!!

        binary, address = self.mySocket.recvfrom(PACKETSIZE)  # Waiting to receive packet from client
        print type(binary)
        print len(binary)
        clientPacket = packet.Packet.unpack(binary)  # Unpack received packet

        print "Le address"
        print address

        sequence_no = random.randint(1, 500)  # Server picks a random sequence number that gets sent to client

        ack_no = clientPacket.ack_no + 1  # Server sends the clients_ack_no + 1 to the client

        print "Ack number is...."
        print ack_no

        returnPacket = packet.Packet(0x0, SYN + ACK, 0x0, sequence_no, ack_no, 0x0)
        binaryData = returnPacket.pack()

        self.mySocket.sendto(binaryData, address) # Do I need to close this socket?!?!?!?!?!?

        con = socket()
        con.connect_address = address
        con.bind(('',8888))  #DON'T FORGET TO BIND

        (clientsocket, address) = (con,address)  # change this to your code
        return (clientsocket,address)

    def close(self):   # fill in your code here
        return

    def send(self,buffer):

        #NEED TO UPDATE ack, seq, packet length, and header length
        header = packet.Packet(0x1, 0x0, PACKETSIZE, self.curr_seq, self.curr_ack, 0x0) # Create header to send

        print "SEND: Buffer Size"
        print len(buffer)

        #self.connect_address[1] = 8888

        addy = (self.connect_address[0],8888)  # Temp port number for TESTING

        bytessent = self.mySocket.sendto(header.pack() + buffer, addy)  # Send header with the payload data

        binary, address = self.mySocket.recvfrom(PACKETSIZE)  # Receive acknowledgement packet

        ack_packet = packet.Packet.unpack(binary)  # acknowledgement packet

        print("ENDING SEND")

        return bytessent - PACKETSIZE  # Need to subtract the header size so you just return the payload length

    def recv(self,nbytes):

        print "IT IS"
        print self.connect_address

       # self.bind(('',8888))

        binary, address = self.mySocket.recvfrom(PACKETSIZE + nbytes)  # Receive packet

        # Separate header data from payload data
        header = binary[:40]
        payload = binary[40:]

        print "Payload size recv"
        print len(payload)

        received_packet = packet.Packet.unpack(header)  # packet header received from sender

        # Create new header to send acknowledgement
        header = packet.Packet(0x1, 0x0, PACKETSIZE, self.curr_seq, self.curr_ack, 0x0)

        print self.connect_address

        self.mySocket.sendto(header.pack(), self.connect_address) # Sending Acknowledgment packet

        print "ENDING RECV"

        return payload  # Return the payload sent


    


