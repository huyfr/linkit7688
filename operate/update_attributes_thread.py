import time

from config import *


def call():
    period = shared_attributes.get('mccPeriodSendTelemetry', default_data.mccPeriodSendTelemetry)
    while True:
        if CLIENT.is_connected():
            update_attributes_lock.acquire()
            gw_client_attributes = format_client_attributes(update_attributes)
            if gw_client_attributes:
                for key, value in gw_client_attributes.items():
                    CLIENT.gw_send_attributes(key, value)
                LOGGER.info('Sent changed client attributes')
                log_info = []
                for key, value in update_attributes.items():
                    log_info.append('\t{:>20s}: {:>20s}'.format(str(key), str(value)))
                LOGGER.info('\n'.join(log_info))
                update_attributes.clear()
            update_attributes_lock.release()
        time.sleep(period)


def replica_client_attributes():
    attributes = {
        "mccCardId": "AAA",
        "mccCardLength": 12,
        "mccRfidConnectState": 1,
        "mccDcCabinetSate": 1,
        "acmTempError": 0,
        "acmHumidError": 0,
        "acmAutoMode": 1,
        "acmOnlineState": 1,
        "acmIState": 1,
        "acmAirc1RunState": 0,
        "acmAirc2RunState": 1,
        "acmAirc1Error": 0,
        "acmAirc2Error": 26,
        "acmFanRunState": 0,
        "acmFanError": 0,
        "atsVacP1State": 0,
        "atsVacP2State": 0,
        "atsVacP3State": 0,
        "atsVgenP1State": 0,
        "atsVgenP2State": 0,
        "atsVgenP3State": 0,
        "atsContactorElecState": 0,
        "atsContactorGenState": 0,
        "atsAcState": 0,
        "atsGenState": 0,
        "atsVacThresholdState": 0,
        "atsVgenThresholdState": 0,
        "atsState": 0,
        "atsErrorState": 0,
        "atsMode": 0
    }

    return attributes


def fake_shared_attributes():
    attributes = {
        "mccPeriodReadDataIO": 0.05,
        "mccPeriodSendShared": 30,
        "mccPeriodSendTelemetry": 50,
        "mccPeriodUpdate": 5,
        "mccListRfid": [],
        "mccDcMinThreshold": 30,
        "acmAlternativeState": 0,
        "acmAlternativeTime": 180,
        "acmRunTime": 240,
        "acmRestTime": 320,
        "acmGenAllow": 1,
        "acmVacThreshold": 180,
        "acmMinTemp": 16,
        "acmMaxTemp": 60,
        "acmMinHumid": 10,
        "acmMaxHumid": 70,
        "acmExpectedTemp": 25,
        "acmExpectedHumid": 45,
        "atsVacMaxThreshold": 180,
        "atsVacMinThreshold": 100,
        "atsVgenMaxThreshold": 120,
        "atsVgenMinThreshold": 600,
        "atsVacStabilizeTimeout": 60,
        "atsVgenIdleCoolingTimeout": 30
    }

    return attributes


def format_client_attributes(dict_attributes):
    list_client_attributes = {DEVICE_MCC: {}, DEVICE_ATS: {}, DEVICE_ACM: {}}
    client_attributes_mcc_1 = {}
    client_attributes_ats_1 = {}
    client_attributes_acm_1 = {}
    data_from_stm32 = dict_attributes

    for key, value in data_from_stm32.items():
        if 'mcc' in key:
            client_attributes_mcc_1[key] = value
        elif 'ats' in key:
            client_attributes_ats_1[key] = value
        elif 'acm' in key:
            client_attributes_acm_1[key] = value

    if client_attributes_ats_1:
        list_client_attributes[DEVICE_ATS] = client_attributes_ats_1
    if client_attributes_acm_1:
        list_client_attributes[DEVICE_ACM] = client_attributes_acm_1
    if client_attributes_mcc_1:
        list_client_attributes[DEVICE_MCC] = client_attributes_mcc_1

    return list_client_attributes


def get_list_key(dict_attributes):
    list_keys = []
    for key in dict_attributes.keys():
        list_keys.append(key)

    return list_keys
