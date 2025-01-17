import serial

import control
from config import *
from config.common_lcd_services import *
from config.common import UPDATE_VALUE, CLEAR, END_CMD
from control.utils import split_row_by_salt
from devices import ats, crmu, clock, acm, mcc
from operate.lcd_thread import extract_lcd_service
from utility import *


bt_info = []
last_stt_bt = 0


def call():
    global bt_info
    # button = Button()

    ser = serial.Serial(port=IO_PORT, baudrate=BAUDRATE)
    data_ack = b'\xa0\x02\x11\x00'
    control_ack = b'\xa0\x01\x21'
    message_break = shared_attributes.get('mccPeriodReadDataIO', default_data.mccPeriodReadDataIO)  # time read data from IO
    flip = READ_PER_WRITE
    flip_lcd = READ_PER_WRITE_LCD

    original_cycle = int((time.time()) / 60)
    while True:
        # Update time clock to IO
        current_cycle = int((time.time()) / 60)
        if not (current_cycle - original_cycle) and not (current_cycle - original_cycle) % 2:
            LOGGER.info("Send clock set")
            clock.set()

        # Read data
        byte_stream = blocking_read(ser, message_break)
        if byte_stream and _read_data(byte_stream):
            ser.write(with_check_sum(data_ack, BYTE_ORDER))

        # read button status
        # try:
        #     if len(bt_info) == 3:
        #         button_status[0] = button.check_button(bt_info)
        #         LOGGER.info('Send button value: %s', LOG_BUTTON[str(button_status[0])])
        # except Exception as ex:
        #     LOGGER.error('Error check button status: %s', ex.message)

        # Write command
        try:
            # lcd
            if cmd_lcd:
                cmd_lcd_snap = []
                if UPDATE_VALUE in cmd_lcd:
                    arr_content = split_row_by_salt(cmd_lcd[UPDATE_VALUE])
                    if len(arr_content) > 0:
                        cmd_lcd_lock.acquire()
                        for item in arr_content:
                            cmd_lcd_snap.append(item)
                        cmd_lcd_lock.release()
                    else:
                        cmd_lcd_lock.acquire()
                        for item in cmd_lcd.items():
                            cmd_lcd_snap.append(item)
                        cmd_lcd_lock.release()
                elif CLEAR in cmd_lcd:
                    cmd_lcd_lock.acquire()
                    for item in cmd_lcd.items():
                        cmd_lcd_snap.append(item)
                    cmd_lcd_lock.release()
                for key_lcd, content in cmd_lcd_snap:
                    cmd_lcd_formatted = {'key_lcd': key_lcd, 'content': content}
                    write_stream = with_check_sum(control.process_cmd_lcd(cmd_lcd_formatted), BYTE_ORDER)
                    tries = 0
                    LOGGER.info('Send cmd lcd to IO, key_lcd %s, content %s', key_lcd, content)
                    while True:
                        if flip == 0:
                            flip = READ_PER_WRITE
                            ser.write(write_stream)
                        else:
                            flip -= 1
                        byte_stream = blocking_read(ser, message_break)
                        if byte_stream:
                            if byte_stream == with_check_sum(control_ack, BYTE_ORDER):
                                cmd_lcd_lock.acquire()
                                del cmd_lcd[key_lcd]
                                cmd_lcd_lock.release()
                                LOGGER.debug("Receive ACK lcd with message with content: %s", content)
                                break
                            if _read_data(byte_stream):
                                ser.write(with_check_sum(data_ack, BYTE_ORDER))
                        if flip == 0:
                            tries += 1
                            if tries > MAX_TRIES:
                                cmd_lcd_lock.acquire()
                                del cmd_lcd[key_lcd]
                                cmd_lcd_lock.release()
                                LOGGER.info('Time out')
                                break
                            LOGGER.debug('Try sending again')
        except Exception as ex:
            LOGGER.error('Error send lcd command to STM32 with message: %s', ex.message)

        try:
            # rpc
            if commands:
                commands_snap = []
                commands_lock.acquire()
                for item in commands.items():
                    commands_snap.append(item)
                commands_lock.release()
                for device, command in commands_snap:
                    command_formatted = {'device': device, 'command': command}
                    write_stream = with_check_sum(control.process_command(command_formatted), BYTE_ORDER)
                    tries = 0
                    LOGGER.info('Send command to IO, device %s, command %s', device, command)
                    while True:
                        if flip == 0:
                            flip = READ_PER_WRITE
                            ser.write(write_stream)
                        else:
                            flip -= 1
                        byte_stream = blocking_read(ser, message_break)
                        if byte_stream:
                            if byte_stream == with_check_sum(control_ack, BYTE_ORDER):
                                commands_lock.acquire()
                                if commands[device] == command:
                                    del commands[device]
                                commands_lock.release()
                                LOGGER.debug("Receive ACK rpc message with device: %s", device)
                                break
                            if _read_data(byte_stream):
                                ser.write(with_check_sum(data_ack, BYTE_ORDER))
                        if flip == 0:
                            tries += 1
                            if tries > MAX_TRIES:
                                commands_lock.acquire()
                                if commands[device] == command:
                                    del commands[device]
                                commands_lock.release()
                                LOGGER.info('Time out')
                                break
                            LOGGER.debug('Try sending again')
        except Exception as ex:
            LOGGER.error('Error send rpc command to STM32 with message: %s', ex.message)

        try:
            # led
            if cmd_led:
                cmd_led_snap = []
                cmd_led_lock.acquire()
                for item in cmd_led.items():
                    cmd_led_snap.append(item)
                cmd_led_lock.release()
                for length_led, arr_value in cmd_led_snap:
                    cmd_led_formatted = {'length_led': length_led, 'arr_value': arr_value}
                    write_stream = with_check_sum(control.process_cmd_led(cmd_led_formatted), BYTE_ORDER)
                    tries = 0
                    LOGGER.info('Send cmd led to IO, length_led: %d, arr_value: %s', length_led, arr_value)
                    while True:
                        if flip == 0:
                            flip = READ_PER_WRITE
                            ser.write(write_stream)
                        else:
                            flip -= 1
                        byte_stream = blocking_read(ser, message_break)
                        if byte_stream:
                            if byte_stream == with_check_sum(control_ack, BYTE_ORDER):
                                cmd_led_lock.acquire()
                                if cmd_led[length_led] == arr_value:
                                    del cmd_led[length_led]
                                cmd_led_lock.release()
                                LOGGER.debug("Receive ACK led message with length_led: %d", length_led)
                                break
                            if _read_data(byte_stream):
                                ser.write(with_check_sum(data_ack, BYTE_ORDER))
                        if flip == 0:
                            tries += 1
                            if tries > MAX_TRIES:
                                cmd_led_lock.acquire()
                                if cmd_led[length_led] == arr_value:
                                    del cmd_led[length_led]
                                cmd_led_lock.release()
                                LOGGER.info('Time out')
                                break
                            LOGGER.debug('Try sending again')
        except Exception as ex:
            LOGGER.error('Error send led command to STM32 with message: %s', ex.message)

        try:
            # shared attributes
            if cmd_sa:
                cmd_sa_snap = []
                cmd_sa_lock.acquire()
                for item in cmd_sa.items():
                    cmd_sa_snap.append(item)
                cmd_sa_lock.release()
                for module_id, value in cmd_sa_snap:
                    cmd_sa_formatted = {'module_id': module_id, 'value': value}
                    write_stream = with_check_sum(control.process_cmd_sa(cmd_sa_formatted), BYTE_ORDER)
                    tries = 0
                    LOGGER.info('Send cmd sa to IO, id_module %s, value %s', module_id, value)
                    while True:
                        if flip == 0:
                            flip = READ_PER_WRITE
                            ser.write(write_stream)
                        else:
                            flip -= 1
                        byte_stream = blocking_read(ser, message_break)
                        if byte_stream:
                            if byte_stream == with_check_sum(control_ack, BYTE_ORDER):
                                cmd_sa_lock.acquire()
                                if cmd_sa[module_id] == value:
                                    del cmd_sa[module_id]
                                cmd_sa_lock.release()
                                LOGGER.debug("Receive ACK shared attributes message with module_id: %d", module_id)
                                break
                            if _read_data(byte_stream):
                                ser.write(with_check_sum(data_ack, BYTE_ORDER))
                        if flip == 0:
                            tries += 1
                            if tries > MAX_TRIES:
                                cmd_sa_lock.acquire()
                                if cmd_sa[module_id] == value:
                                    del cmd_sa[module_id]
                                cmd_sa_lock.release()
                                LOGGER.info('Time out')
                                break
                            LOGGER.debug('Try sending again')
        except Exception as ex:
            LOGGER.error('Error send shared attributes command to STM32 with message: %s', ex.message)


def _read_data(byte_stream):
    global bt_info

    LOGGER.info('Receive data message')
    byte_stream_decode = ':'.join(x.encode('hex') for x in byte_stream)
    LOGGER.info('Byte_stream after decode: %s', byte_stream_decode)
    if len(byte_stream) < 3:
        LOGGER.debug('Message too short, length %d', len(byte_stream))
        return False
    if byte_stream[0] != b'\xa0':
        LOGGER.debug('Mark byte not right, expected mark byte A0, received mark byte %s', byte_stream[0].encode('hex'))
        return False
    # if not check_check_sum(byte_stream, BYTE_ORDER):
    #     LOGGER.debug('Check sum not right, expected check sum %s, received check sum %s',
    #                  with_check_sum(byte_stream[:-2], BYTE_ORDER)[-2:].encode('hex'),
    #                  byte_stream[-2:].encode('hex'))
    #     return False
    frame_length = bytes_to_int(byte_stream[1])
    op_code = byte_stream[2]
    LOGGER.debug('Opcode %s', op_code.encode('hex'))
    data = byte_stream[3:-2]
    if op_code == _OpData.IO_STATUS_ATS:  # ATS
        LOGGER.info('ATS message, declared length: %d, real length: %d, expected length: %d', frame_length - 1,
                    len(data), _OpData.ATS_SIZE)
        if _check_data(frame_length, data, _OpData.ATS_SIZE):
            ats.extract(data)
            return True
    elif op_code == _OpData.IO_STATUS_ACM:  # ACM
        LOGGER.info('ACM message, declared length: %d, real length: %d, expected length: %d', frame_length - 1,
                    len(data), _OpData.ACM_SIZE)
        if _check_data(frame_length, data, _OpData.ACM_SIZE):
            acm.extract(data)
            return True
    elif op_code == _OpData.IO_STATUS_MCC:  # MCC
        LOGGER.info('MCC message, declared length: %d, real length: %d, expected length: %d', frame_length - 1,
                    len(data), _OpData.MCC_SIZE)
        if _check_data(frame_length, data, _OpData.MCC_SIZE):
            LOGGER.info('Check data successful, go to extract MCC')
            mcc.extract(data)
            LOGGER.info('Extract MCC successful')
            return True
    elif op_code == _OpData.IO_STATUS_CRMU:  # CRMU
        LOGGER.info('CRMU message, declared length: %d, real length: %d, expected length: %d', frame_length - 1,
                    len(data), _OpData.CRMU_SIZE)
        if _check_data(frame_length, data, _OpData.CRMU_SIZE):
            crmu.extract(data)
            return True
    elif op_code == _OpData.IO_STATUS_RPC:  # RPC response
        LOGGER.info('RPC message, declared length: %d, real length: %d, expected length: %d', frame_length - 1,
                    len(data), _OpData.RPC_SIZE)
        return True
    elif op_code == _OpData.IO_STATUS_LCD:  # LCD
        LOGGER.info('LCD message, declared length: %d, real length: %d, expected length: %d', frame_length - 1,
                    len(data), _OpData.LCD_SIZE)
        if _check_data(frame_length, data, _OpData.LCD_SIZE):
            # bt_info = data
            extract_lcd_service(data)
            return True
    return False


def _check_data(frame_length, data, expected_data_length):
    LOGGER.info('Enter function _check_data')
    try:
        LOGGER.info('Frame length: %d, data length: %d, expected_data_length: %d', frame_length, len(data),
                    expected_data_length)
        if frame_length != len(data) + 1 or frame_length != expected_data_length:
            LOGGER.info('Frame length != data length + 1 or frame length != expected_data_length')
            LOGGER.info('Exit function _check_data')
            return False
        else:
            LOGGER.info('Compare successful!')
            LOGGER.info('Exit function _check_data')
            return True
    except Exception as ex:
        LOGGER.error('Error at function _check_data with message: %s', ex.message)


class _OpData:
    # current
    ACM_SIZE = 26
    ATS_SIZE = 51
    MCC_SIZE = 58
    CRMU_SIZE = 19
    LCD_SIZE = 4
    RPC_SIZE = 10
    IO_STATUS_MCC = b'\x11'
    IO_STATUS_ATS = b'\x13'
    IO_STATUS_ACM = b'\x14'
    IO_STATUS_CRMU = b'\x16'
    IO_STATUS_RPC = b'\x21'
    IO_STATUS_LCD = b'\x32'

    # new
    # uncomment when update STM32
    # ACM_SIZE = 28
    # ATS_SIZE = 52
    # MCC_SIZE = 58
    # CRMU_SIZE = 19
    # LCD_SIZE = 4
    # RPC_SIZE = 10
    # IO_STATUS_MCC = b'\x11'
    # IO_STATUS_ATS = b'\x13'
    # IO_STATUS_ACM = b'\x14'
    # IO_STATUS_CRMU = b'\x16'
    # IO_STATUS_RPC = b'\x21'
    # IO_STATUS_LCD = b'\x32'


class Button:
    def __init__(self):
        self.button = 0
        self.button_pre = 0

    def check_button(self, bt_info):
        global last_stt_bt
        try:
            LOGGER.info('Enter check_button fucntion')
            key_code = bytes_to_int(bt_info[0:2], byteorder=BYTE_ORDER)
            key_event = bytes_to_int(bt_info[2])
            bt_info = []
            LOGGER.info('After extract command lcd from STM32, key code: %d, key event: %d', key_code, key_event)

            if key_code in LIST_KEYCODE:
                index_key = LIST_KEYCODE.index(key_code)
                LOGGER.info('Key code exist in list key code')

            if key_event == EVENT_UP:
                event = EVENT_UP_BT
            elif key_event == EVENT_HOLD:
                event = EVENT_HOLD_BT
            self.button = event * index_key
            if last_stt_bt != self.button:
                last_stt_bt = self.button
                LOGGER.info('return button value: %s', LOG_BUTTON[str(self.button)])
            return str(self.button)
        except Exception as ex:
            LOGGER.info('check_button function error: %s', ex.message)
