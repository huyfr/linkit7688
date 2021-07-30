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
            LOGGER.debug('Dictionary update client attributes: %s', update_attributes)
            update_attributes_lock.release()
        else:
            LOGGER.debug('Gateway is disconnect from Thingsboard')
        time.sleep(period)


def save_history_client_attributes(dct_client_attributes):
    try:
        dct_latest_client_attributes = dct_client_attributes
        json_latest = json.dumps(dct_latest_client_attributes)
        with io.open('./latest_client_attributes.json', 'wb') as latest_client_attributes_file:
            latest_client_attributes_file.write(json_latest)
        LOGGER.info('Latest client attributes just write to file: %s', dct_latest_client_attributes)
    except Exception as ex:
        LOGGER.error('Error at save_history_client_attributes function with message: %s', ex.message)


def format_client_attributes(dict_attributes):
    list_client_attributes = {DEVICE_MCC: {}, DEVICE_ATS: {}, DEVICE_ACM: {}}
    client_attributes_mcc_1 = {}
    client_attributes_ats_1 = {}
    client_attributes_acm_1 = {}
    try:
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
    except Exception as ex:
        LOGGER.warning('Error at format_client_attributes function with message: %s', ex.message)
    return list_client_attributes


def get_list_key(dict_attributes):
    list_keys = []
    for key in dict_attributes.keys():
        list_keys.append(key)
    return list_keys
