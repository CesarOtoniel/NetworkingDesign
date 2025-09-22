import socket

# Server will listen on port 9000
server_addr = ("127.0.0.1", 9000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_addr)

print("[server] waiting...")

while True:
    data, addr = sock.recvfrom(1024)   # Wait for a message
    print(f"[server] got {data!r} from {addr}")
    sock.sendto(data, addr)            # ECHO the message back
