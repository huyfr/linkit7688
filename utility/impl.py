import time
import struct


# from numba import jit

def bytes_to_int(data, byteorder=None):
    if len(data) == 1:
        return struct.unpack('B', data)[0]
    if byteorder == 'little':
        fmt = '<'
    elif byteorder == 'big':
        fmt = '>'
    else:
        raise ValueError()
    if len(data) == 2:
        return struct.unpack(fmt + 'H', data)[0]
    elif len(data) == 4:
        return struct.unpack(fmt + 'I', data)[0]


def with_check_sum(byte_stream, byteorder):
    return byte_stream + _check_sum(byte_stream, byteorder)


def check_check_sum(byte_stream, byteorder):
    return _check_sum(byte_stream[:-2], byteorder) == byte_stream[-2:]


def blocking_read(ser, message_break):
    initial_break = message_break / 10
    continuous_break = message_break / 100
    result = b''
    time.sleep(initial_break)
    while True:
        time.sleep(continuous_break)
        data_left = ser.inWaiting()
        if data_left > 0:
            result += ser.read(data_left)
        else:
            return result


def _check_sum(byte_stream, byteorder):
    '''
    The function use the crc16 checksum algorithm as follow:
    
        static uint16_t mb_crc16(uint8_t buf[], uint16_t len)
        {
            uint16_t crc16 = 0xFFFF;
            uint16_t i, j, tmp;

            for (i = 0; i < len; ++i) {
                crc16 ^= buf[i];
                for (j = 8; j > 0; --j) {
                    tmp = crc16 & 0x0001;
                    crc16 >>= 1;
                    if (tmp == 1) {
                        crc16 ^= 0xA001;
                    }
                }
            }
            return crc16;
        }
    '''

    length = len(byte_stream)
    crc16 = 0xFFFF
    for i in range(length):
        crc16 ^= bytes_to_int(byte_stream[i])
        for _ in range(8, 0, -1):
            tmp = crc16 & 0x0001
            crc16 >>= 1
            if tmp:
                crc16 ^= 0xA001
    if byteorder == 'little':
        fmt = '<H'
    elif byteorder == 'big':
        fmt = '>H'
    else:
        raise ValueError()
    return struct.pack(fmt, crc16)
