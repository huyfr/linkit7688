import time

from config import *
from config.common_led import *

dct_last_trace_led_alarm = {}


def call():
    period = shared_attributes.get('mccPeriodSendTelemetry', default_data.mccPeriodSendTelemetry)
    while True:
        dct_led_value = get_led_value()
        if len(dct_led_value) > 0:
            compose_led_command(dct_led_value.values())
        time.sleep(period)


def get_led_value():
    dct_led = {}
    try:
        dct_led[LED_SERVER] = get_state_led_server()
        dct_led[LED_ATS] = client_attributes['atsConnect']
        dct_led[LED_DC] = client_attributes['mccDcCabinetSate']
        dct_led[LED_ACM] = client_attributes['acmOnlineState']
        dct_led[LED_ATU] = 0
        dct_led[LED_1] = 0
        dct_led[LED_2] = 0
        dct_led[LED_NONE] = 0
        dct_led[LED_ALARM] = get_sate_led_alarm(dct_alarm)
        dct_led[LED_3G] = 1  # TODO: need function check
        dct_led[LED_ETHERNET] = 1  # TODO: need function check
        dct_led[LED_CRMU] = client_attributes['mccRfidConnectState']
        dct_led[LED_4] = 0
    except Exception as ex:
        LOGGER.error('Error at get_led_value function with message: %s', ex.message)
    return dct_led


def compose_led_command(values):
    arr_led_value = []
    try:
        for i in values:
            checked_value = validate_value(i)
            arr_led_value.append(checked_value)
        cmd_led_lock.acquire()
        cmd_led[LED_LENGTH] = arr_led_value
        cmd_led_lock.release()
    except Exception as ex:
        LOGGER.error('Error at compose_led_command with message: %s', ex.message)


def validate_value(value):
    result = RED
    try:
        if value >= 1:
            result = GREEN
        return result
    except Exception as ex:
        LOGGER.error('Error at validate_value function with message: %s', ex.message)
    return result


def set_last_trace_led_alarm(key, value):
    dct_last_trace_led_alarm[key] = value


def get_sate_led_alarm(dct_telemetry):
    result = -1
    try:
        new_list_telemetries = dict(filter(lambda elem: elem[0].lower().find('state') != -1, dct_telemetry.items()))
        if len(new_list_telemetries) == 0:
            result = 1
        elif len(new_list_telemetries) > 0:
            check = any(elem != 0 for elem in new_list_telemetries.values())
            result = 0 if check else 1
    except Exception as ex:
        LOGGER.error('Error at get_sate_led_alarm function with message: %s', ex.message)
    return result


def get_state_led_server():
    try:
        if CLIENT.is_connected():
            return 1
        else:
            return 0
    except Exception as ex:
        LOGGER.error('Error at get_state_led_server function with message: %s', ex.message)
