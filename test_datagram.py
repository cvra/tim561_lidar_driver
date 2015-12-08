import unittest
from datagram import *
import unittest.mock as mock
from logging import debug


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
        gen = packet_decoder.get_datagram()
        self.assertEqual(next(gen), out1)
        self.assertEqual(next(gen), out2)

    def test_DatagramReaderReceive(self):
        sample = b'\x00'+ETX+b'\x00'+STX+b'\x04'+ETX+b'\x05'+STX+b'\x06'+ETX+b'\x07'+STX+b'\x00'

        mock_socket = mock.Mock()
        mock_socket.recv.return_value = sample

        datagram_reader = DatagramReader(mock_socket)
        data = datagram_reader.receive()
        self.assertEqual(data, sample)

    def test_DatagramReaderReadNext(self):
        sample = b'\x00'+ETX+b'\x00'+STX+b'\x04'+ETX+b'\x05'+STX+b'\x06'+ETX+b'\x07'+STX+b'\x00'
        out1 = STX+b'\x04'+ETX
        out2 = STX+b'\x06'+ETX
        out3 = STX+b'\x00'+b'\x00'+ETX

        mock_socket = mock.Mock()
        mock_socket.recv.return_value = sample

        datagram_reader = DatagramReader(mock_socket)
        datagram_reader.receive()

        datagram = datagram_reader.read_next_datagram()
        self.assertEqual(datagram, out1)

        datagram = datagram_reader.read_next_datagram()
        self.assertEqual(datagram, out2)

        datagram = datagram_reader.read_next_datagram()
        self.assertEqual(datagram, None)

        datagram_reader.receive()
        datagram = datagram_reader.read_next_datagram()
        self.assertEqual(datagram, out3)


class TestDatagramReader(unittest.TestCase):

    example_frame = b'sSN LMDscandata 1 1 E5A5AD 0 0 A9E AA0 BA09FB5 BA0B085 0 0 1 0 0 5DC 12 0 1 DIST1 3F800000 00000000 FFF92230 D05 32B 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 8D A8 B8 C7 CA D2 DC E5 F2 FA F9 F0 F2 F0 F2 FC F8 F9 FE F7 100 103 108 10B 108 112 10F 119 11E 11E 122 125 130 12E 134 14D 16A 17E 184 180 17E 179 174 209 23E 284 A8D 402 3DB 3B8 395 370 354 337 30A 2EE 2D1 2D5 2D7 2D7 2D8 2D7 2D7 2DC 3BE A46 A48 A4A A36 339 34B A4A A4F A30 9F2 9A2 95A 929 36F 3A6 3A4 3A0 3A0 39C 39A 3A0 3A3 3A1 3A7 3A4 3A5 3A4 3A3 3B0 3AF 3B1 3B6 3B8 3C8 2 51E 587 599 58E 59B 1D 57 190 1AD 1A3 1A4 199 198 190 18E 190 190 18E 18B 18B 190 191 18C 18F 191 196 18F 193 190 18E 191 18F 196 198 193 190 193 194 195 198 19C 19F 1A3 1A4 1A4 1A6 1B2 1B1 1B0 1A6 1B0 1AE 1B4 1B3 1B4 1BB 1BF 1C0 1B5 1B1 1BB 1C2 1BC 1C1 1BC 1BD 1BC 1B7 1BF 1BE 1BC 1C5 1BD 1BC 1C8 1C8 1D9 1D9 1CD 1C5 1C9 1CB 1CA 1CD 1E7 1DD 1DB 1D7 1E3 1DD 1D8 1DD 1E1 1E2 1EE 1E2 1F3 1F6 1F7 1EB 203 1FC 1FC 1FE 1F9 200 1F6 202 1FF 1F9 1F5 1EF 1F4 1F0 1FC 1F6 202 1FE 1F8 1FC 205 201 201 20D 207 209 20E 203 20C 20B 205 205 20D 209 20C 213 21C 215 214 219 21F 21E 21D 22A 22F 22A 231 226 229 229 22E 228 220 222 21F 222 222 21C 21D 21E 220 21E 21A 21D 21D 212 21D 219 21E 219 21A 219 214 210 20E 211 216 211 20F 20F 20F 20C 214 209 212 20F 20A 209 209 20A 20F 208 207 207 206 208 20D 202 207 20E 20A 1FE 201 203 20C 208 205 20C 208 20B 20A 20A 207 204 208 206 212 209 203 20F 207 204 20D 20B 210 20A 20B 20A 20D 207 204 20C 20B 20D 200 20C 20C 215 20B 20A 20C 20E 215 215 217 20E 213 21C 215 212 215 214 214 21C 21D 21C 21C 21E 225 21B 228 21C 220 225 228 220 21E 227 230 22A 22B 229 22B 231 22C 230 237 22F 228 233 236 238 23A 239 23F 23E 23F 239 23F 24A 24B 24A 249 250 252 251 250 251 255 256 253 257 263 25F 260 26B 26E 263 26C 26C 26A 26C 274 278 27B 27F 280 287 27F 28A 28B 28E 28A 295 299 298 29A 2A6 29F 2A5 2AB 2A6 2AE 2B4 2BD 2BE 2C1 2BD 2C1 2C6 2C9 2CC 2D2 2D7 2E1 2EA 2EB 2EC 2F5 2F5 2F3 2F5 2F9 2ED 2E3 2E7 2EA 2ED 2E9 2E7 2E0 2DF 2DD 2DA 2D9 2E2 2E0 2D8 2C7 2C3 2C0 2B9 2BA 2BA 2BD 2B8 2B0 2B1 2AC 2AB 2A7 2A8 2AA 2A9 2A7 2A6 2AB 2B0 2BE 2DC 2BD 2B0 2A8 2AF 2AF 2A8 2A0 295 27E 273 26F 26C 269 269 267 25F 248 23B 240 243 249 24F 249 245 242 244 242 23E 23D 23D 243 24E 262 27A 296 2B4 2CB 2D5 315 335 331 363 39E 365 2F9 2EA 300 302 2F2 2EE 2E6 2E7 2E9 2E6 2EA 2E4 2E6 2E2 2E1 2E2 2F5 31E 346 35E 367 360 356 356 354 356 35D 361 367 363 360 35C 357 368 3EF 453 4E0 513 50D 509 506 508 504 502 50B 50D 50B 4FE 507 4FF 504 509 507 4C7 356 32B 330 34D 34F 35F 385 364 372 367 363 364 36E 365 371 372 36F 372 36E 36D 35E 345 363 371 377 379 374 377 37A 376 36C 37A 37B 379 367 335 322 327 325 329 328 32C 32A 329 32E 328 316 30C 2FA 2ED 2E0 2D2 2CB 2C0 2B5 2A7 2A2 295 288 282 274 26E 262 269 259 258 245 23F 234 22A 22E 225 21C 215 212 205 202 1FA 1F8 1F2 1F0 1E9 1E5 1DB 1DA 1DA 1D4 1CA 1C6 1C4 1C0 1C4 1B7 1BB 1B3 1B2 1A7 1A2 1A4 1A5 19C 196 18F 194 193 189 18C 17F 182 17E 17F 17C 17A 172 170 16D 16C 169 166 162 161 160 160 15E 15B 15A 156 155 151 150 14F 14C 14A 149 146 146 146 146 140 141 140 13F 13E 13D 13A 139 137 135 134 132 12D 12F 130 12C 12B 129 129 127 125 123 128 123 11D 114 10D 10A 109 FF E3 B0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 B not defined 0 0 0'

    def test_receive(self):
        sample = b'\x00'+ETX+b'\x00'+STX+b'\x04'+ETX+b'\x05'+STX+b'\x06'+ETX+b'\x07'+STX+b'\x00'

        mock_socket = mock.Mock()
        mock_socket.recv.return_value = sample

        datagram_reader = DatagramReader(mock_socket)
        data = datagram_reader.receive()
        self.assertEqual(data, sample)

    def test_receive_next(self):
        sample = b'\x00'+ETX+b'\x00'+STX+b'\x04'+ETX+b'\x05'+STX+b'\x06'+ETX+b'\x07'+STX+b'\x00'
        out1 = STX+b'\x04'+ETX
        out2 = STX+b'\x06'+ETX
        out3 = STX+b'\x00'+b'\x00'+ETX

        mock_socket = mock.Mock()
        mock_socket.recv.return_value = sample

        datagram_reader = DatagramReader(mock_socket)
        datagram_reader.receive()

        datagram = datagram_reader.read_next_datagram()
        self.assertEqual(datagram, out1)

        datagram = datagram_reader.read_next_datagram()
        self.assertEqual(datagram, out2)

        datagram = datagram_reader.read_next_datagram()
        self.assertEqual(datagram, None)

        datagram_reader.receive()
        datagram = datagram_reader.read_next_datagram()
        self.assertEqual(datagram, out3)

    def test_parse_number_decimal(self):
        self.assertEqual(10, DatagramReader.parse_number(b'+10'))
        self.assertEqual(-10, DatagramReader.parse_number(b'-10'))

    def test_parse_number_hexadecimal(self):
        self.assertEqual(42, DatagramReader.parse_number(b'2A'))

    def test_decode(self):
        decoded = DatagramReader.decode_datagram(TestDatagramReader.example_frame)
        debug(decoded)
        expected = {'TypeOfCommand': 'sSN',
                    'Command': 'LMDscandata',
                    'VersionNumber': 1,
                    'DeviceNumber': 1,
                    'SerialNumber': 'E5A5AD',
                    'DeviceSatus': 0,
                    'TelegramCounter': 0,
                    'AngularStepWidth': 3333,
                    'NumberOfData': 811,
                    'TimeSinceStartup': 0,
                    'TimeOfTransmission': 0}
        self.assertEqual(expected, decoded)



if __name__ == '__main__':
    unittest.main()