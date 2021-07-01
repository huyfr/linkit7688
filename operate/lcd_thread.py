from os import altsep
import time

import requests

from datetime import datetime
from config import *
from config.common import *
from config.common_lcd_services import *
from config.default_data import data_dict
from control import process_cmd_sa, process_cmd_lcd
from devices.utils import read_lcd_services
from model.alarm_lcd import Alarm_lcd
from model.lcd import Lcd
from utility import bytes_to_int

URL_SEND_SA = 'http://123.30.214.139:8517/api/services/app/DMTram/ChangeValueTemplate'
menu_level_1 = [MCC, ACM, ATS]
LIST_KEY_EVENT = [EVENT_NONE, EVENT_DOWN, EVENT_UP, EVENT_HOLD, EVENT_POWER]
LIST_KEY_CODE = [KEYCODE_11, KEYCODE_16, KEYCODE_14, KEYCODE_34, KEYCODE_26, KEYCODE_24, KEYCODE_13, KEYCODE_12]
json_file = open('config/lcd.json')
dct_lcd = json.load(json_file)
dct_lcd_menu = dct_lcd['lcd']['category']['menu']
dct_lcd_menu_level = dct_lcd_menu['level']
dct_lcd_menu_level_lv1 = dct_lcd_menu_level['lv1']
last_alarm_update = Alarm_lcd()
BAN_TIN_CANH_BAO = 'BAN TIN CANH BAO'

def call():
    try:
        period = 3
        # last_trace = get_last_trace()
        while True:
            # check_history_keypad(last_trace)
            result_check_input = check_lcd_service(lcd_services)
            if result_check_input.key_code > 0 and result_check_input.key_event > 0:
                if result_check_input.key_code == KEYCODE_11:
                    cmd_lcd[UPDATE_VALUE] = '' + SALT_DOLLAR_SIGN + str(ROW_3)
                else:
                    result_switch_lcd = switch_lcd_service(result_check_input)
                    cmd_lcd_lock.acquire()

                    # if result_switch_lcd.value < 0:
                    #     cmd_lcd[UPDATE_VALUE] = result_switch_lcd.name + SALT_DOLLAR_SIGN + str(ROW_3)
                    #     show_temp_humi(30, 70)
                    # else:
                    #     cmd_lcd[UPDATE_VALUE] = str(result_switch_lcd.value) + SALT_DOLLAR_SIGN + str(ROW_3)

                cmd_lcd_lock.release()
                set_last_trace(result_switch_lcd)
                lcd_services.clear()
            time.sleep(period)
    except Exception as ex:
        LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)


def check_history_keypad(last_trace):
    if last_trace.key_code == KEYCODE_12:
        check_alarm()


def init_show_alarm():
    cmd_lcd[UPDATE_VALUE] = creat_cmd_rule(BAN_TIN_CANH_BAO, ROW_1)
    check_alarm()


def check_alarm():
    cmd_lcd_dict = {}
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    try:
        max_Tem = shared_attributes.get('acmExpectedTemp', default_data.acmExpectedTemp)
        LOGGER.info('Check Telemetries: %s', telemetries)
        if telemetries:
            if telemetries.get('mccFireState') == 1:
                LOGGER.info('CANH BAO CHAY')
                cmd_lcd_dict[1] = creat_cmd_rule('Canh bao CHAY!', ROW_2)
                cmd_lcd_dict[2] = creat_cmd_rule(dt_string, ROW_3)
            elif telemetries.get('mccSmokeState') == 1:
                LOGGER.info('CANH BAO KHOI')
                cmd_lcd_dict[1] = creat_cmd_rule('Canh bao Khoi!', ROW_2)
                cmd_lcd_dict[2] = creat_cmd_rule(dt_string, ROW_3)
            elif telemetries.get('acmTempIndoor') > max_Tem:
                LOGGER.info('CANH BAO NHIET')
                cmd_lcd_dict[1] = creat_cmd_rule('Canh bao Nhiet!', ROW_2)
                cmd_lcd_dict[2] = creat_cmd_rule(dt_string, ROW_3)
            elif telemetries.get('mccFloodState') == 1:
                LOGGER.info('CANH BAO NGAP')
                cmd_lcd_dict[1] = creat_cmd_rule('Canh bao Ngap!', ROW_2)
                cmd_lcd_dict[2] = creat_cmd_rule(dt_string, ROW_3)
            elif telemetries.get('mccDoorState') == 1:
                LOGGER.info('CANH BAO CUA')
                cmd_lcd_dict[1] = creat_cmd_rule('Canh bao Cua!', ROW_2)
                cmd_lcd_dict[2] = creat_cmd_rule(dt_string, ROW_3)
            elif telemetries.get('mccMoveState') == 1:
                LOGGER.info('CANH BAO CHUYEN DONG')
                cmd_lcd_dict[1] = creat_cmd_rule('CB Chuyen Dong!', ROW_2)
                cmd_lcd_dict[2] = creat_cmd_rule(dt_string, ROW_3)
            else:
                cmd_lcd_dict[1] = creat_cmd_rule('An Toan!', ROW_2)
                cmd_lcd_dict[2] = creat_cmd_rule(' ', ROW_3)

        LOGGER.info('Get list txt row: %s', cmd_lcd_dict)
        multi_cmd_lcd_enable()
        LOGGER.info('Enter show alarm function')
        for i in cmd_lcd_dict:
            add_cmd_lcd(cmd_lcd_dict[i])
        LOGGER.info('Exit show alarm function')
    except Exception as ex:
        LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)


# Button Dieu Hoa
def show_temp_condition():
    cmd_lcd_temp = {}
    cmd_lcd_temp[1] = creat_cmd_rule('BAN TIN DIEU HOA', ROW_1)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    try:
        LOGGER.info('Check Telemetries: %s', telemetries)
        if 'acmAirc1RunState' in telemetries:
            temp1 = telemetries['acmAirc1RunState']
            if temp1 == 0:
                cmd_lcd_temp[2] = creat_cmd_rule('Dieu Hoa1: Tat', ROW_2)
            else:
                cmd_lcd_temp[2] = creat_cmd_rule('Dieu Hoa 1: Bat', ROW_2)
        if 'acmAirc2RunState' in telemetries:
            temp2 = telemetries['acmAirc2RunState']
            if temp2 == 0:
                cmd_lcd_temp[2] = creat_cmd_rule('Dieu Hoa 2: Tat', ROW_3)
            else:
                cmd_lcd_temp[2] = creat_cmd_rule('Dieu Hoa 2: Bat', ROW_3)
        if 'acmAutoMode' in telemetries:
            mode = telemetries['acmAutoMode']
            if mode == 1:
                cmd_lcd_temp[4] = creat_cmd_rule('Che Do: Auto', ROW_4)
            if mode == 0:
                cmd_lcd_temp[4] = creat_cmd_rule('Che Do: Manual', ROW_4)
        LOGGER.info('Get list txt row: %s', cmd_lcd_temp)
        multi_cmd_lcd_enable()
        LOGGER.info('Enter show_tempCondition function')
        for i in cmd_lcd_temp:
            add_cmd_lcd(cmd_lcd_temp[i])
        LOGGER.info('Exit show alarm function')
    except Exception as ex:
        LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)


def switch_lcd_service(input_lcd):
    last_trace = Lcd()
    try:
        key_event = input_lcd.key_event
        key_code = input_lcd.key_code
        if key_event == EVENT_UP:
            if key_code == KEYCODE_16:
                last_trace.category = dct_lcd_menu['id']
                last_trace.level = dct_lcd_menu_level['levelId']
                last_trace.index_level1 = dct_lcd_menu_level_lv1[0]['index']
                last_trace.name = dct_lcd_menu_level_lv1[0]['name']
                last_trace.value = -1
                last_trace.index_level2 = -1
            elif key_code == KEYCODE_14 or key_code == KEYCODE_34:
                last_trace = navigate_lcd_service(key_code)
            elif key_code == KEYCODE_24:
                last_trace = enter_lcd_service()
            elif key_code == KEYCODE_13:
                show_temp_humi(30, 70)
            elif key_code == KEYCODE_12:
                init_show_alarm()
            elif key_event == EVENT_DOWN:
                pass
            elif key_event == EVENT_HOLD:
                pass

            last_trace.key_code = input_lcd.key_code
            last_trace.key_event = input_lcd.key_event
        else:
            LOGGER.info('Key event != EVENT_UP so do nothing')
    except Exception as ex:
        LOGGER.info('Error at switch_lcd_service function with message: %s', ex.message)
    return last_trace


def enter_lcd_service():
    last_trace = get_last_trace()
    try:
        if last_trace.category == KEYCODE_16:
            if last_trace.level == MENU_LEVEL_1:
                last_trace.name = dct_lcd_menu_level_lv1[last_trace.index_level1]['lv2']['keys'][0]
                last_trace.level = dct_lcd_menu_level_lv1[last_trace.index_level1]['lv2']['levelId']
                last_trace.index_level2 = dct_lcd_menu_level_lv1[last_trace.index_level1]['lv2']['keys'].index(
                    last_trace.name)
            elif last_trace.level == MENU_LEVEL_2:
                if last_trace.value == -1:
                    value = shared_attributes.get(last_trace.name, default_data.data_dict['shared'][last_trace.name])
                    last_trace.level = MENU_LEVEL_3
                    last_trace.value = value
            elif last_trace.level == MENU_LEVEL_3:
                body = write_body_send_shared_attributes(last_trace.name, last_trace.value)
                result = send_shared_attributes(body)
                if result:
                    last_trace.value = -1
                    last_trace.level = MENU_LEVEL_2
        else:
            pass
    except Exception as ex:
        LOGGER.error('Error at confirm_lcd_service function with message: %s', ex.message)
    return last_trace


def navigate_lcd_service(key_code):
    index = -1
    last_trace = get_last_trace()
    try:
        if last_trace.category == KEYCODE_16 and last_trace.level == MENU_LEVEL_1:
            if key_code == KEYCODE_14:
                index = last_trace.index_level1 + 1
                if index > dct_lcd_menu_level['maxIndex']:
                    index = dct_lcd_menu_level['minIndex']
            elif key_code == KEYCODE_34:
                index = last_trace.index_level1 - 1
                if index < dct_lcd_menu_level['minIndex']:
                    index = dct_lcd_menu_level['maxIndex']
            last_trace.index_level1 = index
            last_trace.name = dct_lcd_menu_level_lv1[index]['name']
        elif last_trace.category == KEYCODE_16 and last_trace.level == MENU_LEVEL_2:
            if key_code == KEYCODE_14:
                index = last_trace.index_level2 + 1
                if index > dct_lcd_menu_level_lv1[last_trace.index_level1]['lv2']['maxIndex']:
                    index = dct_lcd_menu_level_lv1[last_trace.index_level1]['lv2']['minIndex']
            elif key_code == KEYCODE_34:
                index = last_trace.index_level2 - 1
                if index < dct_lcd_menu_level_lv1[last_trace.index_level1]['lv2']['minIndex']:
                    index = dct_lcd_menu_level_lv1[last_trace.index_level1]['lv2']['maxIndex']
            last_trace.index_level2 = index
            last_trace.name = dct_lcd_menu_level_lv1[last_trace.index_level1]['lv2']['keys'][index]
        elif last_trace.category == KEYCODE_16 and last_trace.level == MENU_LEVEL_3:
            if key_code == KEYCODE_14:
                index = last_trace.value + 1
            elif key_code == KEYCODE_34:
                index = last_trace.value - 1
            last_trace.value = index
    except Exception as ex:
        LOGGER.error('Error at confirm_lcd_service function with message: %s', ex.message)
    return last_trace


def write_body_send_shared_attributes(key, value):
    body = {}
    try:
        now = int(time.time() * 1000)
        body = {"tramEntityId": str(device_config['device_id']), "value": str(value), "keyName": str(key),
                "changeAt": now}
        LOGGER.info('Content of body send shared attributes to Smartsite: %s', body)
    except Exception as ex:
        LOGGER.info('Error at write_body_send_shared_attributes function with message: %s', ex.message)
    return body


def send_shared_attributes(body):
    result = False
    try:
        response = requests.post(url=URL_SEND_SA, json=body)
        if response.status_code == 200:
            LOGGER.info('Send shared attributes to Smartsite successful!')
            result = True
        else:
            LOGGER.info('Fail while send shared attributes to Smartsite!')
    except Exception as ex:
        LOGGER.info('Error at write_log function with message: %s', ex.message)
    return result


def extract_lcd_service(byte_data):
    try:
        key_code = bytes_to_int(byte_data[0:2], byteorder=BYTE_ORDER)
        key_event = bytes_to_int(byte_data[2])
        read_lcd_services('key_code', key_code)
        read_lcd_services('key_event', key_event)
        LOGGER.info('After extract command lcd from STM32, key code: %d, key event: %d', key_code, key_event)
    except Exception as ex:
        LOGGER.error('Error at extract_lcd_service function with message: %s', ex.message)


def get_last_trace():
    lcd_last_trace = Lcd()
    try:
        json_file = open('./last_trace_lcd.json', )
        dct_last_trace = json.load(json_file)
        lcd_last_trace.key_code = dct_last_trace['key_code']
        lcd_last_trace.key_event = dct_last_trace['key_event']
        lcd_last_trace.category = dct_last_trace['category']
        lcd_last_trace.level = dct_last_trace['level']
        lcd_last_trace.index_level1 = dct_last_trace['index_level1']
        lcd_last_trace.index_level2 = dct_last_trace['index_level2']
        lcd_last_trace.value = dct_last_trace['value']
        lcd_last_trace.name = dct_last_trace['name']
    except Exception as ex:
        LOGGER.error('Error at get_last_trace with message: %s', ex.message)
    return lcd_last_trace


def set_last_trace(input_lcd):
    try:
        dct_last_trace = input_lcd.__dict__
        json_last_trace = json.dumps(dct_last_trace)
        with io.open('./last_trace_lcd.json', 'wb') as last_trace_file:
            last_trace_file.write(json_last_trace)
        LOGGER.info('Command information just send: %s', dct_last_trace)
    except Exception as ex:
        LOGGER.error('Error at set_last_trace function with message: %s', ex.message)


def check_lcd_service(dct_lcd_service):
    key_code_checked = False
    key_event_checked = False
    input_lcd = Lcd()
    try:
        input_lcd.key_code = dct_lcd_service['key_code']
        input_lcd.key_event = dct_lcd_service['key_event']

        if input_lcd.key_code in LIST_KEY_CODE:
            key_code_checked = True
            LOGGER.info('Key code: %d, exist in LIST_KEY_CODE', input_lcd.key_code)
        else:
            LOGGER.info('Key code: %d not exists LIST_KEY_CODE', input_lcd.key_code)

        if input_lcd.key_event in LIST_KEY_EVENT:
            key_event_checked = True
            LOGGER.info('Key event: %d exists in LIST_KEY_EVENT', input_lcd.key_event)
        else:
            LOGGER.info('Key event: %d not exists in LIST_KEY_EVENT', input_lcd.key_event)

        if key_code_checked and key_event_checked:
            LOGGER.info('Check key code & key event successful')
        else:
            lcd_services.clear()
            LOGGER.info('Fail while check ')
    except Exception as ex:
        LOGGER.error('Error at check_lcd_service function with message: %s', ex.message)
    return input_lcd


def get_last_alarm():
    last_alarm_trace = Alarm_lcd()
    try:
        json_file = open('./last_trace_alarm_lcd.json', )
        dct_last_trace = json.load(json_file)
        LOGGER.info('after convert from json: %s', dct_last_trace)
        last_alarm_trace.mccDoorState = dct_last_trace['mccDoorState']
        last_alarm_trace.mccFloodState = dct_last_trace['mccFloodState']
        last_alarm_trace.mccSmokeState = dct_last_trace['mccSmokeState']
        last_alarm_trace.mccFireState = dct_last_trace['mccFireState']
        last_alarm_trace.mccMoveState = dct_last_trace['mccMoveState']
        last_alarm_trace.acmTempIndoor = dct_last_trace['acmTempIndoor']
        LOGGER.info('List last alarm: %s', last_alarm_trace)
    except Exception as ex:
        LOGGER.error('Error at get_last_trace with message: %s', ex.message)
    return last_alarm_trace


def set_last_alarm(input_lcd):
    try:
        dct_last_trace = input_lcd.__dict__
        json_last_trace = json.dumps(dct_last_trace)
        with io.open('./last_trace_alarm_lcd.json', 'wb') as last_trace_file:
            last_trace_file.write(json_last_trace)
        LOGGER.info('Command information just send: %s', dct_last_trace)
    except Exception as ex:
        LOGGER.error('Error at set_last_trace function with message: %s', ex.message)


def show_temp_humi(temp, humidity):
    cmd_lcd_dict = {}
    cmd_lcd_dict[0] = creat_cmd_rule(str(temp) + '*C', ROW_3)
    cmd_lcd_dict[1] = creat_cmd_rule(str(humidity) + '%', ROW_4)
    multi_cmd_lcd_enable()
    LOGGER.info('Enter show_temp_humi function')
    for i in cmd_lcd_dict:
        add_cmd_lcd(cmd_lcd_dict[i])
    LOGGER.info('Exit show_temp_humi function')


def multi_cmd_lcd_enable():
    multi_cmd_lcd_flag[0] = True


def multi_cmd_lcd_disable():
    multi_cmd_lcd_flag[0] = False


def add_cmd_lcd(cmd):
    multi_cmd_lcd.append(cmd)


def creat_cmd_rule(string, row):
    cmd = str(string) + SALT_DOLLAR_SIGN + str(row)
    return cmd

# def call():
#     try:
#         period = 3
#         last_trace = get_last_trace()
#         while True:
#             if CLIENT.is_connected():
#                 check_alarm()
#                 result_check_input = check_lcd_service(lcd_services)
#                 if result_check_input.key_code > 0 and result_check_input.key_event > 0:
#                     if result_check_input.key_code == KEYCODE_11:
#                         cmd_lcd[UPDATE_VALUE] = '' + SALT_DOLLAR_SIGN + str(ROW_3)
#                     else:
#                         result_switch_lcd = switch_lcd_service(result_check_input)
#                         cmd_lcd_lock.acquire()
#
#                         # if result_switch_lcd.value < 0:
#                         #     cmd_lcd[UPDATE_VALUE] = result_switch_lcd.name + SALT_DOLLAR_SIGN + str(ROW_3)
#                         #     show_temp_humi(30, 70)
#                         # else:
#                         #     cmd_lcd[UPDATE_VALUE] = str(result_switch_lcd.value) + SALT_DOLLAR_SIGN + str(ROW_3)
#
#                     cmd_lcd_lock.release()
#                     set_last_trace(result_switch_lcd)
#                     lcd_services.clear()
#             time.sleep(period)
#     except Exception as ex:
#         LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)
