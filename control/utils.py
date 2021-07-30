import struct

from config import *
from config.common import *
from config.common_lcd_services import SALT_DOLLAR_SIGN, OP_CODE_SEND_LCD
from config.common_method import *
from control.switcher import *
from control.target import *
from operate.io_thread import ser
from utility import with_check_sum


def _check_command(device, command):
    if device == DEVICE_MCC and (command == GET_STATE or command == GET_VALUE):
        return True
    elif device == DEVICE_ACM and (command == GET_STATE or command == GET_VALUE):
        return True
    elif device == DEVICE_ATS and (command == GET_STATE or command == GET_VALUE):
        return True
    else:
        return False


def check_state_device(device_name, method):
    value = -1
    try:
        if device_name == DEVICE_MCC:
            value = get_state_mcc(method)
        elif device_name == DEVICE_ACM:
            value = get_state_acm(method)
        elif device_name == DEVICE_ATS:
            value = get_state_ats(method)

        if 0 <= value <= 1:
            LOGGER.info('The state of device %s with method %s is: %d', device_name, method, value)
        else:
            LOGGER.info('Status is %d, not as expected', value)
    except Exception as ex:
        LOGGER.error('Error at check_state_device function with message: %s', ex.message)
    return value


def get_state_ats(method):
    value = -1
    try:
        if method == GET_STATE_ATS:
            value = telemetries.get('atsMode', default_data.atsMode)
        elif method == GET_STATE_GEN_ATS:
            value = 0  # TODO: need key for get state of generate
    except Exception as ex:
        LOGGER.error('Error at get_state_ats function with message: %s', ex.message)
    return value


def get_state_acm(method):
    value = -1
    try:
        if method == GET_STATE_ACM_AUTO:
            value = shared_attributes.get('acmControlAuto', default_data.acmControlAuto)
        elif method == GET_SATE_ACM_AIRC_1:
            value = telemetries.get('acmAirc1RunState', default_data.acmAirc1RunState)
        elif method == GET_STATE_ACM_AIRC_2:
            value = telemetries.get('acmAirc2RunState', default_data.acmAirc2RunState)
        elif method == GET_STATE_ACM_FAN:
            value = telemetries.get('acmFanRunState', default_data.acmFanRunState)
        elif method == GET_SATE_ACM_SELF_PROPELLED:
            value = 0
    except Exception as ex:
        LOGGER.error('Error at get_state_acm function with message: %s', ex.message)
    return value


def get_state_mcc(method):
    value = -1
    try:
        if method == GET_STATE_MCC_DOOR:
            value = telemetries.get('mccDoorState', default_data.mccDoorState)
        elif method == GET_STATE_MCC_BELL:
            value = telemetries.get('mccBellState', default_data.mccBellState)
        elif method == GET_STATE_MCC_VMB:
            value = telemetries.get('mccPwRouterState', default_data.mccPwRouterState)
        elif method == GET_STATE_MCC_VSENS:
            value = telemetries.get('mccPwSensState', default_data.mccPwSensState)
        elif method == GET_STATE_MCC_CAM:
            value = telemetries.get('mccPwCamState', default_data.mccPwCamState)
    except Exception as ex:
        LOGGER.error('Error at get_state_mcc function with message: %s', ex.message)
    return value


def get_value_device(device_name, method):
    value = ''
    if device_name == DEVICE_ACM and method == GET_VALUE_ACM_AIRC_1:
        # TODO: change telemetry of airc1:
        value = telemetries.get('acmTempIndoor', default_data.acmTempIndoor)
    elif device_name == DEVICE_ACM and method == GET_VALUE_ACM_AIRC_2:
        # TODO: change telemetry of airc2:
        value = telemetries.get('acmTempOutdoor', default_data.acmTempOutdoor)
    elif device_name == DEVICE_MCC and method == GET_STATE_MCC_DOOR:
        # TODO: change telemetry of airc2:
        value = telemetries.get('mccDoorState', default_data.mccDoorState)
    return value


def _process_set_auto(device, command):
    try:
        if not (type(command) == str and device in [DEVICE_ATS, DEVICE_ACM]):
            return False
        value = convert_str_command_to_int(command)
        if 0 <= value <= 1:
            if device == DEVICE_ACM:
                shared_attributes['acmControlAuto'] = value
            elif device == DEVICE_ATS:
                shared_attributes['atsControlAuto'] = value
        else:
            LOGGER.info('Value: %d, value is not expected', value)
    except Exception as ex:
        LOGGER.error('Error at _process_set_auto function with message: %s', ex.message)
    return True


def _process_command(device, command):
    result = ''
    try:
        if device == DEVICE_MCC or device == DEVICE_ATS or device == DEVICE_ACM:
            result = compose_command_rpc(device, command)
        elif device == RESPONSE_RFID:
            result = struct.pack(FORMAT_RFID, 0xA0, 0x03, 0x24, device, command)
        result_encode = ':'.join(x.encode('hex') for x in result)
        LOGGER.debug('Process command: device: %s, command: %s, after decode is: %s', device, command, result_encode)
    except Exception as ex:
        LOGGER.error('Error at _process_command function with message: %s', ex.message)
    return result


def convert_str_command_to_int(command):
    _command = -1
    if command is COMMAND_ACM_AUTO_ON:
        _command = 1
    elif command is COMMAND_ACM_AUTO_OFF:
        _command = 0
    return _command


def _check_command_send_rpc(device, command):
    result = False
    try:
        if device == DEVICE_ACM and check_exist_command(command):
            result = True
        elif device == DEVICE_ATS and check_exist_command(command):
            result = True
        elif device == DEVICE_MCC and check_exist_command(command):
            result = True
    except Exception as ex:
        LOGGER.error('Error at _check_command_send_rpc function with message: %s', ex.message)
    LOGGER.info('Result of check command is: %s', result)
    return result


def check_exist_command(command):
    result = False
    try:
        if command in list_command:
            result = True
    except Exception as ex:
        LOGGER.error('Error at check_exist_command function with message: %s', ex.message)
    LOGGER.info('Result of check existence is: %s', result)
    return result


def compose_command_rpc(device, command):
    result = -1
    try:
        if device == DEVICE_MCC:
            device = ID_MCC
            command_int = parse_mcc_command_to_number(command)
            target = get_target_by_command_mcc(command)
            if isinstance(command_int, int) and isinstance(target, int) and target >= 0:
                result = struct.pack(FORMAT_RPC, 0xA0, 0x04, 0x21, device, target, command_int)
            else:
                LOGGER.error('Error at device %s with command_int or target is not integer: command_int: %s, target: %s', str(device), str(command_int), str(target))
        elif device == DEVICE_ATS:
            device = ID_ATS
            command_int = parse_ats_command_to_number(command)
            target = get_target_by_command_ats(command)
            if isinstance(command_int, int) and isinstance(target, int) and target >= 0:
                result = struct.pack(FORMAT_RPC, 0xA0, 0x04, 0x21, device, target, command_int)
            else:
                LOGGER.error('Error at device %s with command_int or target is not integer: command_int: %s, target: %s', str(device), str(command_int), str(target))
        elif device == DEVICE_ACM:
            device = ID_ACM
            command_int = parse_acm_command_to_number(command)
            target = get_target_by_command_acm(command)
            if isinstance(command_int, int) and isinstance(target, int) and target >= 0:
                result = struct.pack(FORMAT_RPC, 0xA0, 0x04, 0x21, device, target, command_int)
            else:
                LOGGER.error('Error at device %s with command_int or target is not integer: command_int: %s, target: %s', str(device), str(command_int), str(target))
    except Exception as ex:
        LOGGER.error('Error at compose_command_rpc with message: %s', ex.message)
    if isinstance(result, str):
        byte_stream_decode = ':'.join(x.encode('hex') for x in result)
        LOGGER.info('Command send to STM32: %s', byte_stream_decode)
    else:
        LOGGER.info('Command error!')
    return result


def compose_command_shared_attributes(module_id, value):
    result = -1
    bytes_length = -1
    length = -1
    op_code_sa = 0x41
    try:
        value_checked = check_arr_value(module_id, value)
        length_value = value_checked[-1]
        if module_id == ID_MCC:
            bytes_length = BYTES_SA_MCC
            length = length_value + 3
        elif module_id == ID_ACM:
            bytes_length = BYTES_SA_ACM
            length = length_value + 3
        elif module_id == ID_ATS:
            bytes_length = BYTES_SA_ATS
            length = length_value + 3
        if bytes_length > 0 and length > 0 and len(value_checked) > 0:
            result = struct.pack('BBBBB', 0xA0, length, op_code_sa, module_id, bytes_length)
            for byte in value_checked[0]:
                result += byte
    except Exception as ex:
        LOGGER.error('Error at compose_command_shared_attributes function with message: %s', ex.message)
    return result


def check_arr_value(module_id, value):
    arr_checked = []
    real_length = 0
    try:
        if module_id == ID_MCC:
            for index, item in enumerate(value):
                byte = struct.pack('<H', item)
                arr_checked.append(byte)
                real_length += 2
        elif module_id == ID_ACM:
            for index, item in enumerate(value):
                if index == 1 or index == 2 or index == 3 or index == 5:
                    byte = struct.pack('<H', item)
                    real_length += 2
                else:
                    byte = struct.pack('B', item)
                    real_length += 1
                arr_checked.append(byte)
        elif module_id == ID_ATS:
            for index, item in enumerate(value):
                if index == 5 or index == 8:
                    byte = struct.pack('B', item)
                    real_length += 1
                else:
                    byte = struct.pack('<H', item)
                    real_length += 2
                arr_checked.append(byte)
    except Exception as ex:
        LOGGER.error('Error at check_arr_value function with message %s: ', ex.message)
    return arr_checked, real_length


def compose_command_lcd(row, key_lcd, content):
    try:
        convert_str = str(content)
        str_align_center_line = convert_str.encode('ascii', 'ignore')
        str_split = str_align_center_line.split(SALT_DOLLAR_SIGN)
        str_content = str_split[0].center(16, " ")
        if str_content:
            if key_lcd == UPDATE_VALUE:
                arr_char = [char for char in str_content]
                if len(arr_char) > 16:
                    arr_char = [item for index, item in enumerate(arr_char) if index <= 15]
                elif len(arr_char) < 16:
                    need_add_space = 16 - len(arr_char)
                    postfix = ''.join([char * need_add_space for char in CHAR_SPACE])
                    arr_char.extend([char for char in postfix])
                prefix = ''.join([char * len(arr_char) for char in CHAR_S])
                length = len(arr_char) + 3
                result = struct.pack(FORMAT_LCD + prefix, 0xA0, length, OP_CODE_SEND_LCD, key_lcd, row, *arr_char)
                LOGGER.info('String in LCD success: %s', str_content)
                result_encode = ':'.join(x.encode('hex') for x in result)
                LOGGER.debug('Process lcd command: key_lcd: %s, content: %s, after decode is: %s', key_lcd, content,
                             result_encode)
                resp_write_cmd = write_update_value(result)
                return resp_write_cmd
            elif key_lcd == CLEAR:
                length = 2
                result = struct.pack('BBBB', 0xA0, length, OP_CODE_SEND_LCD, key_lcd)
                LOGGER.info('String in LCD success: %s', str_content)
                result_encode = ':'.join(x.encode('hex') for x in result)
                LOGGER.debug('Process lcd command: key_lcd: %s, content: %s, after decode is: %s', key_lcd, content,
                             result_encode)
                resp_write_cmd = write_update_value(result)
                return resp_write_cmd
        else:
            str_empty = ''.join([char * 16 for char in CHAR_SPACE])
            arr_char = [char for char in str_empty]
            prefix = ''.join([char * len(arr_char) for char in CHAR_S])
            length = len(arr_char) + 3
            row = 3
            result = struct.pack(FORMAT_LCD + prefix, 0xA0, length, OP_CODE_SEND_LCD, key_lcd, row, *arr_char)
            return result
    except Exception as ex:
        LOGGER.error('Error at compose_command_lcd function with message: %s', ex.message)


def _process_cmd_led(length_led, arr_value):
    op_code_led = 0x33
    length_value = len(arr_value)
    length_prefix = length_value + 3
    prefix = ''.join([char * length_prefix for char in CHAR_B])
    try:
        result = struct.pack(prefix, 0xA0, length_led, op_code_led, *arr_value)
        result_encode = ':'.join(x.encode('hex') for x in result)
        LOGGER.debug('Process led command: led_id: %s, led_color: %s, after decode is: %s', length_led, arr_value, result_encode)
        return result
    except Exception as ex:
        LOGGER.error('Error at _process_cmd_led function with message: %s', ex.message)


def _process_cmd_lcd(row, key_lcd, content):
    try:
        result = compose_command_lcd(row, key_lcd, content)
        return result
    except Exception as ex:
        LOGGER.error('Error at _process_cmd_lcd function with message: %s', ex.message)


def _process_cmd_sa(module_id, value):
    result = ''
    try:
        if module_id == ID_MCC or module_id == ID_ACM or module_id == ID_ATS:
            result = compose_command_shared_attributes(module_id, value)
            result_encode = ':'.join(x.encode('hex') for x in result)
            LOGGER.debug('Process sa command: key_name: %s, value: %s, after decode is: %s', module_id, value, result_encode)
        return result
    except Exception as ex:
        LOGGER.error('Error at _process_cmd_lcd function with message: %s', ex.message)


def set_alarm_state_to_dct(dct_telemetry):
    try:
        if len(dct_telemetry) > 0:
            mcc = dct_telemetry.get(DEVICE_MCC)[0]
            acm = dct_telemetry.get(DEVICE_ACM)[0]
            if len(mcc) > 0:
                dct_alarm['mccFireState'] = mcc.get('mccFireState', 0)
                dct_alarm['mccFloodState'] = mcc.get('mccFloodState', 0)
                dct_alarm['mccSmokeState'] = mcc.get('mccSmokeState', 0)
                dct_alarm['mccDoorState'] = mcc.get('mccDoorState', 0)
                dct_alarm['mccDcLowState'] = mcc.get('mccDcLowState', 0)
            if len(acm) > 0:
                dct_alarm['acmTempAlarm'] = acm.get('acmTempAlarm', 0)
                dct_alarm['acmHumidAlarm'] = acm.get('acmHumidAlarm', 0)
        else:
            LOGGER.info('Telemetry is empty!!!')
        LOGGER.info('Dictionary alarm is: %s', dct_alarm)
    except Exception as ex:
        LOGGER.error('Error at set_alarm_state_to_dct function with message: %s', ex.message)


def write_update_value(bytes_command):
    result = False
    try:
        write_stream = with_check_sum(bytes_command, BYTE_ORDER)
        response = ser.write(write_stream)
        if response > 0:
            result = True
        LOGGER.info('Response when send command UPDATE_VALUE: %s', str(response))
    except Exception as ex:
        LOGGER.error('Error at function write_update_value with message: %s', ex.message)
    return result


def write_to_json(body, file_url):
    try:
        json_last_trace = json.dumps(body)
        with io.open(file_url, 'wb') as last_trace_file:
            last_trace_file.write(json_last_trace)
        LOGGER.info('Command information just send: %s', body)
    except Exception as ex:
        LOGGER.error('Error at write_to_json function with message: %s', ex.message)


def read_to_json(file_url):
    try:
        json_file = open(file_url, )
        json_info = json.load(json_file)
    except Exception as ex:
        LOGGER.error('Error at call function in read_to_json with message: %s', ex.message)
    return json_info


def validate_log_level(sa_log_level):
    level = -1
    try:
        if isinstance(sa_log_level, int):
            if sa_log_level == 1:
                level = logging.DEBUG
            elif sa_log_level == 2:
                level = logging.INFO
            elif sa_log_level == 3:
                level = logging.WARNING
            elif sa_log_level == 4:
                level = logging.ERROR
            elif sa_log_level == 5:
                level = logging.CRITICAL
            else:
                level = sa_log_level
            LOGGER.debug('Log level declared on server is: %s', str(level))
        else:
            LOGGER.warning('Log level get from server is not number')
    except Exception as ex:
        LOGGER.warning('Error at validate_log_level function with message: %s', ex.message)
    return level
