import socket   #socket library
import struct
import os       #os and for system calls and directory usage
import sys

SERVER_ADDR = ("127.0.0.1", 9100) #localhost address
CHUNK = 1024    #size of the udp payload

def send_start(sock, path):         #start of the payload
    fn = os.path.basename(path).encode("utf-8") 
    size = os.path.getsize(path)
    pkt = b"STRT" + struct.pack(">H", len(fn)) + fn + struct.pack(">Q", size)
    sock.sendto(pkt, SERVER_ADDR)
    return size

def send_data(sock, b):             #indicates data packet
    pkt = b"DATA" + struct.pack(">I", len(b)) + b
    sock.sendto(pkt, SERVER_ADDR)

def send_end(sock):                 #indicates end of the payload
    sock.sendto(b"END!", SERVER_ADDR)

def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <file_to_send>")
        sys.exit(1)

    path = sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    size = send_start(sock, path)
    print(f"[client] sending {path} ({size} bytes)")

    sent = 0
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            send_data(sock, chunk)
            sent += len(chunk)

    send_end(sock)
    print(f"[client] done: sent {sent} bytes (RDT 1.0)")

if __name__ == "__main__":
    main()
