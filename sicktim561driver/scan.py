import socket
from sicktim561driver import *
import zmqmsgbus


if __name__ == '__main__':
    bus = zmqmsgbus.Bus(sub_addr='ipc://ipc/source',
                        pub_addr='ipc://ipc/sink')

    node = zmqmsgbus.Node(bus)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.10.3", 2112))
    # activate stream
    s.send(b'\x02sEN LMDscandata 1\x03\0')

    datagrams_generator = datagrams_from_socket(s)

    while 1:
        datagram = next(datagrams_generator)
        decoded = decode_datagram(datagram)

        node.publish('/lidar/scan', decoded)