import socket
from datagram import DatagramReader

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.1", 2112))
# activate stream
s.send(b'\x02sEN LMDscandata 1\x03\0')

datagram_reader = DatagramReader(s)

while 1:
    datagram_reader.receive()
    datagram = datagram_reader.readNextDatagram()

    print(readNextDatagram + "\n\n")

