import time

from config import *
from control.utils import set_alarm_state_to_dct

disconnected = False


def call():
    global disconnected
    from operate.main_thread import disconnect_thingsboard
    period = shared_attributes.get('mccPeriodSendTelemetry', default_data.mccPeriodSendTelemetry)
    while True:
        try:
            if CLIENT.is_connected():
                telemetry = format_telemetry(telemetries)
                for key, value in telemetry.items():
                    response = CLIENT.gw_send_telemetry(key, value)
                    LOGGER.info('RC of send telemetry to Thingsboard is: %s', str(response.rc()))
                    if response.rc() != 0:
                        if disconnected:
                            disconnect_thingsboard(DEVICE_MCC, DEVICE_ATS, DEVICE_ACM)
                            disconnected = False
                set_alarm_state_to_dct(telemetry)
                disconnected = True
                LOGGER.debug('Dictionary telemetries: %s', telemetries)
            else:
                LOGGER.debug('Gateway is disconnected!')
                if disconnected:
                    disconnect_thingsboard(DEVICE_MCC, DEVICE_ATS, DEVICE_ACM)
                    disconnected = False
            time.sleep(period)
        except Exception as ex:
            LOGGER.warning('Error at call function in telemetry_thread with message: %s', ex.message)


def save_history_telemetry(dct_telemetry):
    try:
        dct_latest_telemetry = dct_telemetry
        json_latest = json.dumps(dct_latest_telemetry)
        with io.open('./latest_telemetry.json', 'wb') as latest_telemetry_file:
            latest_telemetry_file.write(json_latest)
        LOGGER.info('Latest telemetry just write to file: %s', dct_latest_telemetry)
    except Exception as ex:
        LOGGER.warning('Error at save_history_telemetry function with message: %s', ex.message)


def format_telemetry(dict_telemetry):
    list_telemetry = {DEVICE_MCC: [{}], DEVICE_ATS: [{}], DEVICE_ACM: [{}]}
    telemetry_mcc_1 = {}
    telemetry_ats_1 = {}
    telemetry_acm_1 = {}
    try:
        data_from_stm32 = dict_telemetry
        for key, value in data_from_stm32.items():
            if 'mcc' in key:
                telemetry_mcc_1[key] = value
            elif 'ats' in key:
                telemetry_ats_1[key] = value
                if 'atsVacP1' == key or 'atsVacP2' == key or 'atsVacP3' == key:
                    telemetry_ats_1['atsVacAlarm'] = check_vac_alarm_ats(value)
            elif 'acm' in key:
                telemetry_acm_1[key] = value
                if 'acmTempIndoor' == key:
                    telemetry_acm_1['acmTempAlarm'] = check_temp_alarm_acm(value)
                elif 'acmHumidIndoor' == key:
                    telemetry_acm_1['acmHumidAlarm'] = check_humid_alarm_acm(value)
        if telemetry_mcc_1:
            list_telemetry[DEVICE_MCC] = [telemetry_mcc_1]
        if telemetry_ats_1:
            list_telemetry[DEVICE_ATS] = [telemetry_ats_1]
        if telemetry_acm_1:
            list_telemetry[DEVICE_ACM] = [telemetry_acm_1]
    except Exception as ex:
        LOGGER.warning('Error format_telemetry function with message: %s', ex.message)
    return list_telemetry


def check_temp_alarm_acm(value):
    result = 0
    try:
        max_temp_threshold = shared_attributes.get('acmMaxTempThreshold', default_data.acmMaxTempThreshold)
        if value > max_temp_threshold:
            result = 2
        min_temp_threshold = shared_attributes.get('acmMinTempThreshold', default_data.acmMinTempThreshold)
        if value < min_temp_threshold:
            result = 1
    except Exception as ex:
        LOGGER.warning('Error at check_alarm_acm function with message: %s', ex.message)
    return result


def check_humid_alarm_acm(value):
    result = 0
    try:
        max_humid_threshold = shared_attributes.get('acmMaxHumidThreshold', default_data.acmMaxHumidThreshold)
        if value > max_humid_threshold:
            result = 2
        min_humid_threshold = shared_attributes.get('acmMinHumidThreshold', default_data.acmMinHumidThreshold)
        if value < min_humid_threshold:
            result = 1
    except Exception as ex:
        LOGGER.warning('Error at check_humid_alarm_acm function with message: %s', ex.message)
    return result


def check_vac_alarm_ats(value):
    result = 0
    try:
        max_vac_threshold = shared_attributes.get('atsVacMaxThreshold', default_data.atsVacMaxThreshold)
        if value > max_vac_threshold:
            result = 2
        min_vac_threshold = shared_attributes.get('atsVacMinThreshold', default_data.atsVacMinThreshold)
        if value < min_vac_threshold:
            result = 1
    except Exception as ex:
        LOGGER.warning('Error at check_vac_alarm_ats function with message: %s', ex.message)
    return result
