# client.py
# PA1 Network Packet Handling
# Alexis Ouelltte

import argparse
import socket
import struct

def create_packet(version, header_length, service_type, payload):
# Implement packet creation based on parameters
    payload_bytes = b''

    #for integer
    if service_type == 1: 
        payload_bytes = struct.pack('!i', int(payload))
    #for float
    elif service_type == 2: 
        payload_bytes = struct.pack('!f', float(payload))
    #for string     
    elif service_type == 3:
        payload_bytes == payload.encode('utf-8')
    #error
    else:
        raise ValueError("Error")

    #payload length is the length of the bytes being sent
    payload_length = len(payload_bytes)

    header_format = '!BBBH'
    header = struct.pack(header_format, version, header_length, service_type, payload_length)

    return header + payload_bytes

# use the python struct module to create a fixed length header
# Fixed length header -> Version (1 byte), Header Length (1 byte) Service Type (1 byte), Payload Length (2 bytes)
# payload -> variable length
#depending on the service type, handle encoding of the different types of payload.
#  service_type 1 = payload is int, service_type 2 = payload isfloat, service_type 3 = payload is stringreturn packet

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Client for packet creation and sending.")
    parser.add_argument('--version', type=int, required=True, help='Packet version')
    parser.add_argument('--header_length', type=int, required=True, help='Length of the packet header')
    parser.add_argument('--service_type', type=int, required=True, help='Service type of the payload (1 for int, 2 for float, 3 for string)') 
    parser.add_argument('--payload', type=str, required=True, help='Payload to be packed into the packet')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=12345, help='Server port')

    args = parser.parse_args()

    # Create and send packet using the create_packet function
    packet = create_packet(args.version, args.header_length, args.service_type, args.payload)
    
    #connect to the server and send the packet
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            #connect to server
            s.connect((args.host, args.port))
            print(f"Connected to server at {args.host}:{args.port}.")

            #send packet
            s.sendall(packet)
            print("The packet has been sent to the server.")

            #recieve the packet and print the payload
            echoed_packet = s.recv(1024)
            print(f"Recieved from the server {echoed_packet.decode('utf-8')}")
        
        #check for error
        except Exception as e:
            print(f"Error: {e}")
