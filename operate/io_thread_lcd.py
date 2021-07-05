import serial

import control
from config import *
from control.utils import split_list_by_row
from utility import with_check_sum, blocking_read


def call():
    ser = serial.Serial(port=IO_PORT, baudrate=BAUDRATE)
    message_break = shared_attributes.get('mccPeriodReadDataIO', default_data.mccPeriodReadDataIO)
    flip = READ_PER_WRITE
    while True:
        try:
            # lcd
            if cmd_lcd:
                cmd_lcd_snap = []
                cmd_lcd_lock.acquire()
                for item in cmd_lcd.items():
                    cmd_lcd_snap.append(item)
                cmd_lcd_lock.release()
                list_cmd = split_list_by_row(cmd_lcd_snap)
                if len(list_cmd) > 0:
                    for row, key_lcd, content in list_cmd:
                        write_stream = with_check_sum(control.process_cmd_lcd(row, key_lcd, content), BYTE_ORDER)
                        tries = 0
                        LOGGER.info('Send cmd lcd to IO, row %s, key_lcd %s, content %s', row, key_lcd, content)
                        while True:
                            if flip == 0:
                                flip = READ_PER_WRITE
                                ser.write(write_stream)
                            else:
                                flip -= 1
                            byte_stream = blocking_read(ser, message_break)
                            if byte_stream:
                                cmd_lcd_lock.acquire()
                                if cmd_lcd[key_lcd] == content:
                                    del cmd_lcd[key_lcd]
                                cmd_lcd_lock.release()
                                LOGGER.debug("Receive ACK lcd with message with content: %s", content)
                                break
                            if flip == 0:
                                tries += 1
                                if tries > MAX_TRIES:
                                    cmd_lcd_lock.acquire()
                                    if cmd_lcd[key_lcd] == content:
                                        del cmd_lcd[key_lcd]
                                    cmd_lcd_lock.release()
                                    LOGGER.info('Time out')
                                    break
                                LOGGER.debug('Try sending again')
                else:
                    LOGGER.info('Length of list_cmd = 0')
        except Exception as ex:
            LOGGER.error('Error send lcd command to STM32 with message: %s', ex.message)
