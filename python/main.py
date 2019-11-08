import os
from argparse import ArgumentParser

from serial_connector import SerialConnector

connector = SerialConnector()

parser = ArgumentParser()

connector.add_arguments(parser)

if __name__ == '__main__':
    print('hi')
    args = parser.parse_args()
    args = {
        'port': args.port,
        'baud': args.baud,
        'dry': args.dry,
    }
    connector.run(**args)
