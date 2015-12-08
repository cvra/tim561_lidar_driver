import unittest
from datagram import *
import unittest.mock as mock

STX = b'\x02'
ETX = b'\x03'

class TestPacketDecoder(unittest.TestCase):
    def test_basic(self):
        packet_decoder = PacketDecoder()
        buff = b'\x02sEN LMDscandata 1\x03\0'
        packet_decoder.feed(buff)

    def test_decode(self):
        packet_decoder = PacketDecoder()

        sample = b'\x00'+ETX+b'\x00'+STX+b'\x04'+ETX+b'\x05'+STX+b'\x06'+ETX+b'\x07'+STX+b'\x00'
        out1 = STX+b'\x04'+ETX
        out2 = STX+b'\x06'+ETX

        packet_decoder.feed(sample)
        gen = packet_decoder.getDatagram()
        self.assertEqual(next(gen), out1)
        self.assertEqual(next(gen), out2)

    def test_DatagramReaderReceive(self):
        sample = b'\x00'+ETX+b'\x00'+STX+b'\x04'+ETX+b'\x05'+STX+b'\x06'+ETX+b'\x07'+STX+b'\x00'

        mock_socket = mock.Mock()
        attrs = {'recv.return_value': sample}
        mock_socket.configure_mock(**attrs)

        datagram_reader = DatagramReader(mock_socket)
        data = datagram_reader.receive()
        self.assertEqual(data, sample)

    def test_DatagramReaderReadNext(self):
        sample = b'\x00'+ETX+b'\x00'+STX+b'\x04'+ETX+b'\x05'+STX+b'\x06'+ETX+b'\x07'+STX+b'\x00'
        out1 = STX+b'\x04'+ETX
        out2 = STX+b'\x06'+ETX
        out3 = STX+b'\x00'+b'\x00'+ETX

        mock_socket = mock.Mock()
        attrs = {'recv.return_value': sample}
        mock_socket.configure_mock(**attrs)

        datagram_reader = DatagramReader(mock_socket)
        datagram_reader.receive()

        datagram = datagram_reader.readNextDatagram()
        self.assertEqual(datagram, out1)

        datagram = datagram_reader.readNextDatagram()
        self.assertEqual(datagram, out2)

        datagram = datagram_reader.readNextDatagram()
        self.assertEqual(datagram, None)

        datagram_reader.receive()
        datagram = datagram_reader.readNextDatagram()
        self.assertEqual(datagram, out3)




if __name__ == '__main__':
    unittest.main()