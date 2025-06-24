# Alexis Ouellette
# Program Assignment 2 - Simple Protocol
# lightserver.py 

import socket
import argparse
import struct
import logging

#recv_all function takes the socket to be read and then the bytes in the socket and returns the data
def recv_all(sock, length):
    #empty object to store the number of bytes received
    data = b''  
    #while loop to collect all the bytes
    while len(data) < length:
        #get the number of bytes needed
        packet = sock.recv(length - len(data))
        #return None so the program doesn't get stuck
        if not packet:
            return None
        #add all the data together 
        data += packet
    #return new data thats been stored
    return data

def main():
    #server takes 2 arguements - p: PORT, l: log file location 
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="Port to listen on")
    parser.add_argument("-l", required=True, help="Log file location")
    args = parser.parse_args()

    #logging messages
    logging.basicConfig(
        level=logging.INFO, 
        format='%(message)s',
        handlers=[
            logging.FileHandler(args.l),
            logging.StreamHandler()
        ])

    #creating a new socket object for the server to use on IPv4 (af_inet) and TCP (sock_stream)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #binding the socket to the IP address and the port for it to make the new connection
    server_socket.bind(('', args.p))
    #telling the socket to listen for the new connection 
    server_socket.listen()

    #logging message
    logging.info(f"Server started on Port {args.p}")

    #while loop for accepting the new clients
    while True: 
        #client socket connects and the server socket accepts it returns the IP and Port address 
        client_socket, addr = server_socket.accept()
        logging.info(f"Received connection from (IP, PORT):  {addr}")

        #connects to the 12 byte header and breaks if not found
        while True:
            header = recv_all(client_socket, 12)
            if not header: 
                break

            #getting the version, message type, and the number of bytes 
            version, msg_type, msg_len = struct.unpack(">III", header)

            #logging message
            logging.info(f"Received Data: version: {version} message_type: {msg_type} length: {msg_len}")
            
            #checks which version was accepted
            if version == 17:
                logging.info("VERSION ACCEPTED")
            else:
                logging.error("VERSION MISMATCH")
                continue

            #reads and decodes the bytes sent from the client 
            message = recv_all(client_socket, msg_len)
            if not message: 
                break

            message_str = message.decode()

            #logging messages depending on which version was received
            if msg_type == 0:
                logging.info("Received Message Hello")
                reply = struct.pack(">III", 17, 0, 5) + b"HELLO"
                client_socket.sendall(reply)
            elif msg_type == 1: 
                logging.info("EXECUTING SUPPORTED COMMAND: LIGHTON")
                reply = struct.pack(">III", 17, 1, 7) + b"SUCCESS"
                client_socket.sendall(reply)
                logging.info("Returning SUCCESS")
            elif msg_type == 2: 
                logging.info("EXECUTING SUPPORTED COMMAND: LIGHTOFF")
                reply = struct.pack(">III", 17, 1, 7) + b"SUCCESS"
                client_socket.sendall(reply)    
                logging.info("Returning SUCCESS")
            else: 
                logging.info(f"IGNORNING UNKNOWN COMMAND: {message_str}")

        #close the client socket
        client_socket.close()
        
if __name__ == "__main__":
    main()
