import os
from argparse import ArgumentParser

from serial_connector import SerialConnector

connector = SerialConnector()

parser = ArgumentParser()

parser.add_argument(
    '-p', '--port',
    type=str,
    dest='port',
    help='Device location, e.g. /dev/ttyUSBx or COMx',
    default=None
)
parser.add_argument(
    '-b', '--baud',
    dest='baud',
    type=str,
    help='Baudrate (default 115200)',
    default=9600
)
parser.add_argument(
    '--dry',
    dest='dry',
    action='store_true')

if __name__ == '__main__':
    args = parser.parse_args()
    args = {
        'port': args.port,
        'baud': args.baud,
        'dry': args.dry,
    }
    connector.run(**args)
