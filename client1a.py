import socket

server_addr = ("127.0.0.1", 9000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send HELLO
msg = b"HELLO"
sock.sendto(msg, server_addr)
print(f"[client] sent {msg!r}")

# Receive ECHO
data, addr = sock.recvfrom(1024)
print(f"[client] got echo {data!r} from {addr}")
