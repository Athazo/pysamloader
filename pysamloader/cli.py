#!/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012-2019 Chintalagiri Shashank
#
# This file is part of pysamloader.

# pysamloader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pysamloader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pysamloader.  If not, see <http://www.gnu.org/licenses/>.


import logging
import argparse
import importlib

from serial.tools import list_ports

from .terminal import ProgressBar
from .pysamloader import get_supported_devices
from .pysamloader import write_and_verify

logger = logging.getLogger('cli')


def print_supported_devices():
    print("Supported devices : ")
    for d in get_supported_devices():
        print(" - {0}".format(d[0]))


def print_serial_ports():
    print("Detected serial ports : ")
    for p in list_ports.comports():
        print(" - {0:15} {1:20} {2:18} {3:18}"
              "".format(str(p.device), str(p.manufacturer),
                        str(p.product), str(p.serial_number)))


def _get_parser():
    parser = argparse.ArgumentParser(
        description="Write an Atmel SAM chip's Flash using SAM-BA over UART")
    parser.add_argument('-g', action='store_true',
                        help="Set GPNVM bit when done writing. Needed to "
                             "switch device boot from SAM-BA ROM to Flash "
                             "program")
    parser.add_argument('-v', action='store_true',
                        help="Verbose debug information")
    parser.add_argument('-c', action='store_true',
                        help="Verify Only. Do not write")
    parser.add_argument('filename', metavar='file', nargs='?',
                        help="Binary file to be burnt into the chip")
    parser.add_argument('--port', metavar='port', default="/dev/ttyUSB1",
                        help="Port on which SAM-BA is listening. "
                             "Default /dev/ttyUSB1")
    parser.add_argument('--baud', metavar='baud', type=int, default=115200,
                        help="Baud rate of serial communication. "
                             "Default 115200")
    parser.add_argument('-d', '--device', metavar='device',
                        help="ARM Device. Default ATSAM3U4E")
    parser.add_argument('--lp', '--list-ports', action='store_true',
                        help="List available serial ports")
    parser.add_argument('--ld', '--list-devices', action='store_true',
                        help="List supported devices")
    return parser


def main():
    parser = _get_parser()
    arguments = parser.parse_args()

    if arguments.v:
        logger.setLevel(logging.DEBUG)
        logging.getLogger('pysamloader').setLevel(logging.DEBUG)
        logging.getLogger('samba').setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        logging.getLogger('pysamloader').setLevel(logging.INFO)
        logging.getLogger('samba').setLevel(logging.INFO)

    if arguments.lp:
        return print_serial_ports()

    if arguments.ld:
        return print_supported_devices()

    if not arguments.filename:
        print("No bin file provided and no list actions requested.")
        parser.print_help()
        return

    if not arguments.device:
        logger.info("Device not specified. Assuming ATSAM3U4E.")
        arguments.device = 'ATSAM3U4E'

    try:
        dev_mod = importlib.import_module(
            '.devices.{0}'.format(arguments.device), 'pysamloader')
        dev = getattr(dev_mod, arguments.device)()
    except ImportError:
        from .samdevice import SAMDevice
        dev = SAMDevice()
        logger.warning("Device is not supported!")
        print_supported_devices()

    arguments.device = dev
    write_and_verify(arguments, progress_class=ProgressBar)


if __name__ == "__main__":
    main()