# Simple Protocol – Light Control Client/Server

This project implements a basic TCP-based client-server protocol for controlling a virtual light. The protocol uses structured headers and logs all communication between a client and server to log files.

## Files

### `lightclient.py`
A TCP client that sends a handshake followed by a command (`LIGHTON` or `LIGHTOFF`) to the server and receives confirmation.

### `lightserver.py`
A TCP server that listens for client connections and responds to `HELLO`, `LIGHTON`, and `LIGHTOFF` commands.

### `output_lightclient.txt`
Sample log file showing the client-side communication sequence, responses, and results.

### `output_lightserver.txt`
Sample log file showing the server-side communication, accepted commands, and execution.

### `sp.pcap` 
A packet capture (PCAP) file showing network activity between the client and server for analysis using Wireshark or tcpdump.

---

## How It Works

Communication is based on a simple protocol:
- All messages start with a 12-byte header:
  - `version` (4 bytes, integer)
  - `msg_type` (4 bytes, integer)
  - `msg_length` (4 bytes, integer)
- This is followed by a UTF-8 encoded message body.

### Message Types:
- `0`: HELLO message
- `1`: LIGHTON command
- `2`: LIGHTOFF command

The server only accepts version 17.

---

## Running the Programs
### 1. Start the Server
python lightserver.py -p 12345 -l output_lightserver.txt
-p: Port to listen on (e.g. 12345)
-l: Path to save server logs

### 2. Run the Client
python lightclient.py -s 127.0.0.1 -p 12345 -l output_lightclient.txt --command LIGHTON
-s: IP address of the server
-p: Port number to connect to
-l: Path to save client logs
--command: Command to send (LIGHTON or LIGHTOFF)

### Capture the Packet Flow
Use capture.pcap to visualize packet flow in tools like Wireshark. It shows:
- TCP 3-way handshake
- HELLO packet exchange
- Command and response
- TCP FIN (close)

### Requirements
Python 3.6+
No external libraries (uses built-in socket, argparse, struct, and logging)

### Notes
Only version 17 is accepted for communication.
Unknown commands are logged and ignored.
Both client and server handle partial socket reads with recv_all().

### Author
Lexi Ouellette
Project: Computer Networking Class – Networking Lab Protocol Assignment 

### Security Warning
This protocol does not implement encryption or authentication. It's intended for educational use only.
