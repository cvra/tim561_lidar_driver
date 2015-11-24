import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.1", 2112))
# activate stream
s.send(b'\x02sEN LMDscandata 1\x03\0')

while True:
    print(s.recv(1000))
