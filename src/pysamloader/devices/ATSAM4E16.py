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


import samdevice


class ATSAM4E16(samdevice.SAMDevice):
    EFC_FMR = '400E0A00'
    EFC_FCR = '400E0A04'
    EFC_FSR = '400E0A08'
    EFC_FRR = '400E0A0C'
    CHIPID_CIDR = '400E0740'
    CHIPID_EXID = '400E0744'
    AutoBaud = False
    FullErase = False
    WP_COMMAND = '01'
    EWP_COMMAND = '03'
    EA_COMMAND = '05'
    FS_ADDRESS = '00400000'
    PAGE_SIZE = 512
    SGPB_CMD = '0B'
    CGPB_CMD = '0C'
    GD_CMD = '00'
    STUI_CMD = '0E'
    SPUI_CMD = '0F'
    SGP = [0, 1, 0]

    def __init__(self):
        super(ATSAM4E16, self).__init__()

if __name__ == '__main__':
    dev = ATSAM4E16()
