import os
import subprocess
import time

from serial import Serial, SerialException
from serial.tools import list_ports

from api_connector import send_measurement
from measurement import Measurement


class SerialConnector(object):
    help = 'Starts the serial read of the smart meter'

    def add_arguments(self, parser):
        parser.add_argument(
            '-p', '--port',
            dest='port',
            type=str,
            help='Device location, e.g. /dev/ttyUSBx or COMx',
            default='/dev/ttyUSB0',
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

    def get_port(self, initial):
        available_ports = list_ports.comports()
        if len(available_ports) == 0:
            return None
        return next(port.device for port in available_ports if port.device == initial) or available_ports[0].device

    def run(self, *args, initial_port=None, baud=None, dry=None):
        port = self.get_port(initial_port)
        ser = Serial(port, baud)

        measurement = Measurement()

        while 1:
            try:
                while not ser.is_open:
                    port = self.get_port(initial_port)
                    print('.', end='', flush=True)
                    if port:
                        ser.setPort(port)
                        try:
                            ser.open()
                            print('Serial connected', port, baud)
                            break
                        except SerialException as e:
                            print('\n', e)
                    time.sleep(5)
                serial_line = ser.readline().decode("utf-8")
                measurement.parse_line(serial_line)
                if measurement.completed:
                    if measurement.is_complete():
                        if dry:
                            print(measurement.as_dict())
                        else:
                            ok = send_measurement(measurement)
                            print('measurement send,', ok)
                    measurement = Measurement()

            except KeyboardInterrupt:
                print('Serial reader closed, keyboard interrupt')
                ser.close()
                break

            except SerialException as e:
                print('Serial exception', e)
                ser.close()

            except Exception:
                # Something went very wrong ?? Very dirty fix for now
                update_script = '/home/pi/update.sh'
                if os.path.isfile(update_script):
                    subprocess.call(update_script)
