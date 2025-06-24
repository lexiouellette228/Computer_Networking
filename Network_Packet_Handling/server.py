# server.py
# Network Packet Handling

import socket
import struct

# Define packet to unpack
def unpack_packet(conn, header_format):
    # recieve the header
    header_size = struct.calcsize(header_format)
    header_data = conn.recv(header_size)

    # check for no data and returns none if no data is found
    if not header_data: 
        return None
    
    # unpacking the header based on the bytes recieved
    version, header_length, service_type, payload_length = struct.unpack(header_format, header_data)

    # get the payload from the length of the payload
    payload_data = conn.recv(payload_length)
    if not payload_data:
        return None

    # create a string from the header fields
    packet_header_as_string = (
        f"Version: {version}, Header length: {header_length}, "
        f"Service Type: {service_type}, Payload length: {payload_length}, "
        f"Payload: {payload_data.decode('utf-8')}"
    )

    # return the string - this will be the payload
    return packet_header_as_string

if __name__ == '__main__':
    host = '10.128.0.2' #my VM internal IP address
    port = 12345

# Fixed length header -> Version (1 byte), Header Length (1 byte), 
# Service Type (1 byte), Payload Length (2 bytes)
# Specify the header format using "struct"
# header set to 4
header_format = '!BBBH' 

# Create the socket for the connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by: {addr}")
        while True:
            try:
            # receive and unpack packet using the unpack_packet
                payload_string = unpack_packet(conn, header_format)

            # break after data is loaded
                if payload_string is None:
                    break

                print("recieved packet: ", payload_string)

            # echo back to client
                conn.sendall(payload_string.encode('utf-8'))

            # check for error
            except Exception as e:
                print("Error")
                break
