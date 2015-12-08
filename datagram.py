import socket
from struct import *
import collections

sick561_datagram = collections.namedtuple("sick561_datagram", ["TypeOfCommand", 
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
                                                               "Datas",
                                                               "NumberOf8BitChannels",
                                                               "Position",
                                                               "Name",
                                                               "Comment",
                                                               "TimeInformation",
                                                               "EventInformation"])

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
        if not self._gen:
            self._gen = self._decoder.get_datagram()

        datagram = next(self._gen, None)
        if datagram == None:
            self._gen = None

        self.last_datagram = datagram
        return datagram

    def decode_datagram(self, datagram):
        fmt = '3s11s2HI4H2I5H2I2H5s2fI9H'
        sick561_datagram._make(unpack(fmt, datagram))
