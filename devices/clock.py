import os
import time
import serial
import datetime
import struct

from config import *
from utility import bytes_to_int, with_check_sum, check_check_sum, blocking_read


def set():
    '''
    Set the clock of the IO sync with the clock of the CORE
    '''
    LOGGER.debug('Send time info to IO')
    ser = serial.Serial(port=IO_PORT, baudrate=BAUDRATE)
    message_break = shared_attributes.get('mccPeriodReadDataIO', default_data.mccPeriodReadDataIO)  # time read data from IO
    flip = READ_PER_WRITE
    while True:
        if flip == 0:
            flip = READ_PER_WRITE
            now = int(time.time() + 25200)
            if BYTE_ORDER == 'little':
                fmt = '<'
            elif BYTE_ORDER == 'big':
                fmt = '>'
            else:
                raise AssertionError()
            message = struct.pack(fmt + 'BBBI', 0xA0, 0x05, 0x02, now)
            ser.write(with_check_sum(message, BYTE_ORDER))
        else:
            flip -= 1
        response = blocking_read(ser, message_break)
        if response == with_check_sum(b'\xa0\x01\x02', BYTE_ORDER):
            LOGGER.debug('Receive ACK clock message')
            break
        if flip == 0:
            LOGGER.debug('Time out, try again')
    ser.close()


def extract():
    '''
    Sync the clock of the CORE with the clock of the IO
    '''
    LOGGER.debug('Get time info from IO')
    ser = serial.Serial(port = IO_PORT, baudrate = BAUDRATE)
    message_break = default_data.mccPeriodReadDataIO
    flip = READ_PER_WRITE
    while True:
        if flip == 0:
            flip = READ_PER_WRITE
            ser.write(with_check_sum(b'\xa0\x01\x01', BYTE_ORDER))
        else:
            flip -= 1
        byte_stream = blocking_read(ser, message_break)
        if _handle(byte_stream):
            LOGGER.debug('Receive time info from IO')
            break
        if flip == 0:
            LOGGER.debug('Failed, try again')
    ser.close()


def _handle(byte_stream):
    '''
    Change the time after receiving the time from IO
    '''
    LOGGER.debug('Handle time info message')
    if len(byte_stream) != 9:
        return False
    if byte_stream[:3] != b'\xa0\x05\x01':
        return False
    if not check_check_sum(byte_stream, BYTE_ORDER):
        return False
    time = bytes_to_int(byte_stream[3:7], byteorder = BYTE_ORDER)
    iso_time = datetime.datetime.fromtimestamp(time).isoformat().replace('T', ' ')
    if '.' in iso_time:
        iso_time = iso_time[:iso_time.find('.')]
    os.system('date -s ' + iso_time)
    return True
