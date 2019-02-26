
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
global recive_port

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here
    transmit_port= UDPportTx
    recive_port = UDPportRx

class socket:
    
    def __init__(self):  # fill in your code here
        self.mySocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
        self.connect_address = None  # Address socket is connecting to
       # self.mySocket.settimeout(2)
        return
    
    def bind(self,address):
        self.mySocket.bind(address)
        return 

    def connect(self,address):  # fill in your code here
        print "In the connect function...."

        sequence_no = random.randint(1, 500)


        connectPacket = packet.Packet(0x1, SYN, 0x0, sequence_no, 0x0, 0x0)  # Creating packet to send
        binaryData = connectPacket.pack()  # Pack into binary data

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
        clientPacket = packet.Packet.unpack(binary)  # Unpack received packet

        print "Le address"
        print address

        print "Syn + Ack bit is...."
        print SYN + ACK

        sequence_no = random.randint(1, 500)  # Server picks a random sequence number that gets sent to client

        ack_no = clientPacket.ack_no + 1  # Server sends the clients_ack_no + 1 to the client

        print "Ack number is...."
        print ack_no

        returnPacket = packet.Packet(0x0, SYN + ACK, 0x0, sequence_no, ack_no, 0x0)
        binaryData = returnPacket.pack()

        self.mySocket.sendto(binaryData, address) # Do I need to close this socket?!?!?!?!?!?

        con = socket()
        con.connect_address = address
       # con.bind(('',1112))

        (clientsocket, address) = (con,address)  # change this to your code
        return (clientsocket,address)
    
    def close(self):   # fill in your code here 
        return 

    def send(self,buffer):
        bytessent = 0
        #bytessent = self.mySocket.sendto(buffer, self.connect_address)



        return bytessent

    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here

        return bytesreceived 


    


