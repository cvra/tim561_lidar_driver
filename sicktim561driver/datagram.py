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

def bytes_from_socket(socket):
    while True:
        data = socket.recv(256)
        for byte in data:
            yield bytes([byte])

def datagrams_from_socket(socket):
    STX = b'\x02'
    ETX = b'\x03'

    byte_generator = bytes_from_socket(socket)

    while True:
        datagram = b''

        for byte in byte_generator:
            if byte == STX:
                break

        for byte in byte_generator:
            if byte == ETX:
                break
            datagram += byte
        yield datagram

def parse_number(nbr_str):
    """ decimal numbers are encoded with leading +/- """
    if b'+' in nbr_str or b'-' in nbr_str:
        return int(nbr_str)
    else:
        return int(nbr_str, 16)

def decode_datagram(datagram):
    items = datagram.split(b' ')

    header = {}
    header['TypeOfCommand'] = items[0].decode('ascii')
    if header['TypeOfCommand'] != 'sSN':
        return None
    header['Command'] = items[1].decode('ascii')
    if header['Command'] != 'LMDscandata':
        return None
    header['VersionNumber'] = parse_number(items[2])
    header['DeviceNumber'] = parse_number(items[3])
    header['SerialNumber'] = items[4].decode('ascii')
    header['DeviceStatus1'] = parse_number(items[5])
    header['DeviceStatus2'] = parse_number(items[6])
    if header['DeviceStatus1'] != 0 or header['DeviceStatus2'] != 0:
        return None
    header['TelegramCounter'] = parse_number(items[7])
    header['TimeSinceStartup'] = parse_number(items[9])
    header['TimeOfTransmission'] = parse_number(items[10])
    header['AngularStepWidth'] = parse_number(items[24])
    header['NumberOfData'] = parse_number(items[25])
    header['Data'] = [parse_number(x) / 1000 for x in items[26:26+header['NumberOfData']]]

    return header

