import time

from config import *
from config.common import *


def call():
    period = shared_attributes.get('periodUpdate', default_data.periodUpdate)
    while True:
        if CLIENT.is_connected():
            update_attributes_lock.acquire()
            gw_client_attributes = format_attributes(update_attributes)
            gw_shared_attributes = format_attributes(shared_attributes)
            if gw_client_attributes:
                for key, value in gw_client_attributes.items():
                    CLIENT.gw_send_attributes(key, value)
                if gw_shared_attributes:
                    for key, value in gw_shared_attributes.items():
                        CLIENT.gw_send_attributes(key, value)
                LOGGER.info('Sent changed client attributes')
                log_info = []
                for key, value in update_attributes.items():
                    log_info.append('\t{:>20s}: {:>20s}'.format(str(key), str(value)))
                LOGGER.info('\n'.join(log_info))
                update_attributes.clear()
            update_attributes_lock.release()
        time.sleep(period)


def format_attributes(dict_attributes):
    list_client_attributes = {DEVICE_MDC_1: {}, DEVICE_MCC_1: {}, DEVICE_ATS_1: {}, DEVICE_ACM_1: {}}
    client_attributes_mdc_1 = {}
    client_attributes_mcc_1 = {}
    client_attributes_ats_1 = {}
    client_attributes_acm_1 = {}
    data_from_stm32 = dict_attributes

    for key, value in data_from_stm32.items():
        if 'crmu' in key:
            client_attributes_mdc_1[key] = value
        elif 'ats' in key:
            client_attributes_ats_1[key] = value
        elif 'airc' in key:
            client_attributes_acm_1[key] = value
        else:
            client_attributes_mcc_1[key] = value

    if client_attributes_mdc_1:
        list_client_attributes[DEVICE_MDC_1] = client_attributes_mdc_1
    if client_attributes_ats_1:
        list_client_attributes[DEVICE_ATS_1] = client_attributes_ats_1
    if client_attributes_acm_1:
        list_client_attributes[DEVICE_ACM_1] = client_attributes_acm_1
    if client_attributes_mcc_1:
        list_client_attributes[DEVICE_MCC_1] = client_attributes_mcc_1

    return list_client_attributes


def get_list_key(dict_attributes):
    list_keys = []
    for key in dict_attributes.keys():
        list_keys.append(key)

    return list_keys
