import time

from config import *
from control.utils import set_alarm_state_to_dct


def call():
    period = shared_attributes.get('mccPeriodSendTelemetry', default_data.mccPeriodSendTelemetry)
    while True:
        if CLIENT.is_connected():
            if len(telemetries) > 0:
                telemetry = format_telemetry(telemetries)
                for key, value in telemetry.items():
                    response = CLIENT.gw_send_telemetry(key, value)
                    LOGGER.info('RC of send telemetry to Thingsboard is: %s', str(response.rc()))
                    if response.rc() != 0:
                        CLIENT.disconnect()
                LOGGER.info('Sent telemetry data')
                log_info = []
                for key, value in telemetries.items():
                    log_info.append('\t{:>20s}: {:>20s}'.format(str(key), str(value)))
                LOGGER.info('\n'.join(log_info))
                LOGGER.info('Dictionary telemetries: %s', telemetries)
                set_alarm_state_to_dct(telemetries)
            else:
                LOGGER.info('Telemetry is empty!!!')
        time.sleep(period)


def save_history_telemetry(dct_telemetry):
    try:
        dct_latest_telemetry = dct_telemetry
        json_latest = json.dumps(dct_latest_telemetry)
        with io.open('./latest_telemetry.json', 'wb') as latest_telemetry_file:
            latest_telemetry_file.write(json_latest)
        LOGGER.info('Latest telemetry just write to file: %s', dct_latest_telemetry)
    except Exception as ex:
        LOGGER.error('Error at save_history_telemetry function with message: %s', ex.message)


def replica_telemetry():
    telemetry = {
        "mccSmokeState": 1,
    "mccFireState": 19,
    "mccMoveState": 60,
    "mccDoorState": 0,
    "mccBellState": 0,
    "mccFloodState": 0,
    "mccDcIbat1": 0,
    "mccDcVbat1": 0,
    "mccDcBat1Temp": 0,
    "mccDcBat2Temp": 13,
    "mccDcBat3Temp": 16,
    "mccDcBat4Temp": 19,
    "mccDoorButton": 0,
    "mccDcAccuState": 0,
    "mccDcVcabinet": 0,
    "mccDcIcabinet": 0,
    "mccDcPcabinet": 0,
    "mccDcPaccumulator": 0,
    "mccSystemClock": 0,
    "mccNetworkParam": {},
    "acmTempIndoor": 35,
    "acmTempOutdoor": 85,
    "acmHumidIndoor": 30,
    "atsVacFreq": 13,
    "atsVgenFreq": 17,
    "atsVloadFreq": 23,
    "atsVacP1": 220,
    "atsVacP2": 10,
    "atsVacP3": 11,
    "atsVgenP1": 10,
    "atsVgenP2": 11,
    "atsVgenP3": 12,
    "atsVloadP1": 20,
    "atsVloadP2": 21,
    "atsVloadP3": 22,
    "atsIloadP1": 24,
    "atsIloadP2": 21,
    "atsIloadP3": 22,
    "atsPac1": 22,
    "atsPac2": 24,
    "atsPac3": 25

    }

    return telemetry


def format_telemetry(dict_telemetry):
    list_telemetry = {DEVICE_MCC: [{}], DEVICE_ATS: [{}], DEVICE_ACM: [{}]}
    telemetry_mcc_1 = {}
    telemetry_ats_1 = {}
    telemetry_acm_1 = {}
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

    return list_telemetry


def check_temp_alarm_acm(value):
    result = 0
    try:
        if 'acmMaxTempThreshold' in shared_attributes:
            max_temp_threshold = shared_attributes['acmMaxTempThreshold']
            if value > max_temp_threshold:
                result = 2
                LOGGER.info('Temperature indoor > acmMaxTempThreshold')
            else:
                LOGGER.info('Temperature indoor < acmMaxTempThreshold')
        else:
            LOGGER.info('No acmMaxTempThreshold key in shared attributes')
        if 'acmMinTempThreshold' in shared_attributes:
            min_temp_threshold = shared_attributes['acmMaxTempThreshold']
            if value < min_temp_threshold:
                result = 1
                LOGGER.info('Temperature indoor < acmMinTempThreshold')
            else:
                LOGGER.info('Temperature indoor > acmMinTempThreshold')
        else:
            LOGGER.info('No acmMinTempThreshold key in shared attributes')
    except Exception as ex:
        LOGGER.error('Error at check_alarm_acm function with message: %s', ex.message)
    return result


def check_humid_alarm_acm(value):
    result = 0
    try:
        if 'acmMaxHumidThreshold' in shared_attributes:
            max_humid_threshold = shared_attributes['acmMaxHumidThreshold']
            if value > max_humid_threshold:
                result = 2
                LOGGER.info('Humidity indoor > acmMaxHumidThreshold')
            else:
                LOGGER.info('Humidity indoor < acmMaxHumidThreshold')
        else:
            LOGGER.info('No acmMaxHumidThreshold key in shared attributes')
        if 'acmMinHumidThreshold' in shared_attributes:
            min_humid_threshold = shared_attributes['acmMinHumidThreshold']
            if value < min_humid_threshold:
                result = 1
                LOGGER.info('Humidity indoor < acmMinHumidThreshold')
            else:
                LOGGER.info('Humidity indoor > acmMinHumidThreshold')
        else:
            LOGGER.info('No acmMinHumidThreshold key in shared attributes')
    except Exception as ex:
        LOGGER.error('Error at check_humid_alarm_acm function with message: %s', ex.message)
    return result


def check_vac_alarm_ats(value):
    result = 0
    try:
        if 'atsVacMaxThreshold ' in shared_attributes:
            max_vac_threshold = shared_attributes['atsVacMaxThreshold ']
            if value > max_vac_threshold:
                result = 2
                LOGGER.info('VAC > atsVacMaxThreshold')
            else:
                LOGGER.info('VAC indoor < atsVacMaxThreshold')
        else:
            LOGGER.info('No atsVacMaxThreshold key in shared attributes')
        if 'atsVacMinThreshold ' in shared_attributes:
            min_vac_threshold = shared_attributes['atsVacMinThreshold ']
            if value < min_vac_threshold:
                result = 1
                LOGGER.info('VAC < atsVacMinThreshold')
            else:
                LOGGER.info('VAC > atsVacMinThreshold')
        else:
            LOGGER.info('No atsVacMinThreshold key in shared attributes')
    except Exception as ex:
        LOGGER.error('Error at check_vac_alarm_ats function with message: %s', ex.message)
    return result

