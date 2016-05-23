import socket
from sicktim561driver import *
import zmqmsgbus
import numpy as np

TIM561_START_ANGLE = 2.3561944902   # -135° in rad
TIM561_STOP_ANGLE = -2.3561944902   #  135° in rad

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
        
        if decoded is not None:
            node.publish('/lidar/radius', decoded['Data'])
            node.publish('/lidar/theta', np.linspace(TIM561_START_ANGLE, TIM561_STOP_ANGLE, len(decoded['Data'])).tolist())