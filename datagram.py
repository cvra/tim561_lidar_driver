import collections
from logging import debug

Sick561Datagram = collections.namedtuple("sick561_datagram", ["TypeOfCommand",
                                                               "Command",
                                                               "VersionNumber",
                                                               "DeviceNumber",
                                                               "SerialNumber",
                                                               "DeviceSatus1",
                                                               "DeviceSatus2",
                                                               "TelegramCounter",
                                                               "ScanCounter",
                                                               "TimeSinceStartup",
                                                               "TimeOfTransmission",
                                                               "InputStatus1",
                                                               "InputStatus2",
                                                               "OutputStatus1",
                                                               "OutputStatus2",
                                                               "ScanningFrequency",
                                                               "MeasurementFrequency",
                                                               "NumberOfEncoders",
                                                               "NumberOf16bitChannels",
                                                               "MeasuredDataContents",
                                                               "ScalingFactor",
                                                               "ScalingOffset",
                                                               "StartingAngle",
                                                               "AngularStepWidth",
                                                               "NumberOfData",
                                                               "Data"])
                                                               # "NumberOf8BitChannels",
                                                               # "Position",
                                                               # "Name",
                                                               # "Comment",
                                                               # "TimeInformation",
                                                               # "EventInformation"])

class PacketDecoder():
    STX = b'\x02'
    ETX = b'\x03'

    def __init__(self):
        self._stream = b''

    def feed(self, buffer):
        self._stream += buffer

    def get_datagram(self):
        '''
        Yields packets from the current stream.
        '''
        while len(self._stream) > 2:
            start = self._stream.find(self.STX)
            if start == -1:
                break

            end = self._stream.find(self.ETX, start)
            if end == -1:
                break

            packet = self._stream[start:end+1]
            yield packet
            self._stream = self._stream[end+1:]


class DatagramReader():
    def __init__(self, socket):
        self._socket = socket
        self._decoder = PacketDecoder()
        self._gen = None

    def receive(self):
        data = self._socket.recv(256)
        self._decoder.feed(data)
        return data

    def read_next_datagram(self):
        datagram = None
        while datagram is None:
            if not self._gen:
                self._gen = self._decoder.get_datagram()

            datagram = next(self._gen, None)
            if datagram == None:
                self._gen = None
                self.receive()

        datagram = datagram.lstrip(PacketDecoder.STX)
        datagram = datagram.rstrip(PacketDecoder.ETX)
        return datagram

    @staticmethod
    def parse_number(nbr_str):
        """ decimal numbers are encoded with leading +/- """
        if b'+' in nbr_str or b'-' in nbr_str:
            return int(nbr_str)
        else:
            return int(nbr_str, 16)

    @staticmethod
    def decode_datagram(datagram):
        items = datagram.split(b' ')
        debug(items)
        debug(len(items))

        parse_number = DatagramReader.parse_number

        header = {}
        header['TypeOfCommand'] = items[0].decode('ascii')
        header['Command'] = items[1].decode('ascii')
        header['VersionNumber'] = parse_number(items[2])
        header['DeviceNumber'] = parse_number(items[3])
        header['SerialNumber'] = items[4].decode('ascii')
        header['DeviceSatus'] = parse_number(items[5])
        header['TelegramCounter'] = parse_number(items[6])
        header['TimeSinceStartup'] = parse_number(items[7])
        header['TimeOfTransmission'] = parse_number(items[8])
        header['AngularStepWidth'] = parse_number(items[24])
        header['NumberOfData'] = parse_number(items[25])

        return header

        # fmt = '3s11s2HI4H2I5H2I2H5s2fI2H'
        # return Sick561Datagram._make(unpack(fmt, datagram[0:88]))
