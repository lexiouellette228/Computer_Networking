# Simple Protocol
# lightclient.py 

import socket
import argparse
import struct
import logging

# recv_all function takes the socket to be read and then the bytes in the socket and returns the data
def recv_all(sock, length):
    # empty object to store the number of bytes received
    data = b''  
    # while loop to collect all the bytes
    while len(data) < length:
        #get the number of bytes needed
        packet = sock.recv(length - len(data))
        #return None so the program doesn't get stuck
        if not packet:
            return None
        # add all the data together 
        data += packet
    # return new data thats been stored
    return data

def main(): 
    # Client takes 3 arguments - s: server IP, p: PORT, -l: log file location 
    # --command: to switch between LIGHTON and LIGHTOFF
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", required=True, help="Server IP")
    parser.add_argument("-p", type=int, required=True, help="Port to connect to")
    parser.add_argument("-l", required=True, help="Log file location")
    parser.add_argument("--command", choices=["LIGHTON", "LIGHTOFF"], required=True, help="Command to send")
    args = parser.parse_args()

    # Logging messages
    logging.basicConfig(
        level=logging.INFO, 
        format='%(message)s',
        handlers=[
            logging.FileHandler(args.l),
            logging.StreamHandler()
        ])

    # Connect to the server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        s.connect((args.s, args.p))

        # sending hello packet
        logging.info("Sending HELLO packet")
        hello_msg = b"HELLO"
        hello_header = struct.pack(">III", 17, 0, len(hello_msg))
        s.sendall(hello_header + hello_msg)

        # receiving Hello response
        header = recv_all(s, 12)
        if not header:
            logging.info("Connection closed by server.")
            return

        # Unpacking the header and making into 4 byte integers and logging the results
        version, msg_type, msg_len = struct.unpack(">III", header)
        logging.info(f"Received Data: version: {version} type: {msg_type} length: {msg_len}")

        # logging version messagees
        if version == 17:
            logging.info("VERSION ACCEPTED")
        else: 
            logging.info("VERSION MISMATCH")

        body = recv_all(s, msg_len)
        if body:
            logging.info("Received Message " + body.decode())

        # send LIGHTON or LIGHTOFF command
        logging.info("Sending command")
        command_bytes = args.command.encode()
        command_type = 1 if args.command == "LIGHTON" else 2
        cmd_header = struct.pack(">III", 17, command_type, len(command_bytes))
        s.sendall(cmd_header + command_bytes)

        # receive the success message
        header = recv_all(s, 12)
        if not header: 
            logging.info("No response received from command")
            return
        
        # reads the header with big endian order and logs the results 
        version, msg_type, msg_len = struct.unpack(">III", header)
        logging.info(f"Received data: version: {version} type: {msg_type} length: {msg_len}")
        logging.info("VERSION ACCEPTED")

        # reads the message body from the socket and logs the result 
        body = recv_all(s, msg_len) 
        if body: 
            logging.info("Received Message " + body.decode())

        # logging closing messages 
        logging.info("Command Successful")
        logging.info("Closing Socket")

if __name__ == "__main__":
    main()
