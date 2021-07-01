import time

from config import *


def call():
    period = shared_attributes.get('mccPeriodSendTelemetry', default_data.mccPeriodSendTelemetry)
    while True:
        if CLIENT.is_connected():
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
            telemetries_lock.acquire()
            telemetries.clear()
            telemetries_lock.release()
        time.sleep(period)


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
    "atsPac3": 25,
    "acmAirc1RunState": 0,
    "acmAirc2RunState": 1,
    "acmAutoMode": 1,
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
        elif 'acm' in key:
            telemetry_acm_1[key] = value

    if telemetry_mcc_1:
        list_telemetry[DEVICE_MCC] = [telemetry_mcc_1]
    if telemetry_ats_1:
        list_telemetry[DEVICE_ATS] = [telemetry_ats_1]
    if telemetry_acm_1:
        list_telemetry[DEVICE_ACM] = [telemetry_acm_1]

    return list_telemetry
