#!/usr/bin/env python3
import socket
import struct
import os

SERVER_ADDR = ("127.0.0.1", 9100) #Localhost on a port greater than 1024
BUF = 1500  # fits typical MTU

def recv_exact_tag(sock, tag):    #implements tag on data as described in textbook
    data, addr = sock.recvfrom(BUF)
    if not data.startswith(tag):
        raise RuntimeError(f"expected {tag}, got {data[:4]!r}")
    return data, addr

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SERVER_ADDR)
    print(f"[server] listening on {SERVER_ADDR}")

    # 1) START
    pkt, sender = recv_exact_tag(sock, b"STRT")
    # parse: "STRT" + 2B name_len + name + 8B size
    name_len = struct.unpack(">H", pkt[4:6])[0]
    name = pkt[6:6+name_len].decode("utf-8", "strict")
    file_size = struct.unpack(">Q", pkt[6+name_len:6+name_len+8])[0]
    out_name = f"recv_{os.path.basename(name)}"
    f = open(out_name, "wb")
    print(f"[server] start recv: {name} ({file_size} bytes) -> {out_name}")

    received = 0
    while True:
        pkt, _ = sock.recvfrom(BUF)
        tag = pkt[:4]
        if tag == b"DATA":
            chunk_len = struct.unpack(">I", pkt[4:8])[0]
            chunk = pkt[8:8+chunk_len]
            f.write(chunk)
            received += len(chunk)
            if received >= file_size:
                # we may still get END!, but file is complete under rdt1.0 assumption
                pass
        elif tag == b"END!":
            print(f"[server] done, wrote {received} bytes")
            break
        else:
            raise RuntimeError(f"unexpected tag {tag!r}")

    f.close()
    print("[server] closed")

if __name__ == "__main__":
    main()
