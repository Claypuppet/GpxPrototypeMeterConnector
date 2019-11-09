import os
from argparse import ArgumentParser

from .serial_connector import SerialConnector

connector = SerialConnector()

parser = ArgumentParser()

parser.add_argument(
    '-p', '--port',
    dest='port',
    type=str,
    help='Device location, e.g. /dev/ttyUSBx or COMx',
    default=None
)
parser.add_argument(
    '-b', '--baud',
    dest='baud',
    type=str,
    help='Baudrate (default 115200)',
    default=115200
)
parser.add_argument(
    '--dry',
    dest='dry',
    action='store_true')

if __name__ == '__main__':
    args = parser.parse_args()
    connector.run(initial_port=args.port, baud=args.baud, dry=args.dry)
