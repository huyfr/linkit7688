import time
from operator import itemgetter

from config import *
from config.common import *
from control.switcher import *


list_dict_ats = []
list_dict_acm = []
list_dict_mcc = []

def call():
    try:
        period = 60
        while True:
            if CLIENT.is_connected():
                for key, value in shared_attributes.items():
                    response_classify_sa = classify_shared_attributes(key, value)
                    if len(response_classify_sa) > 0:
                        if response_classify_sa[ID_SHARED_ATTRIBUTES] > 0:
                            classify_dict(response_classify_sa)
                response_sorted = sort_list_dict(list_dict_mcc, list_dict_acm, list_dict_ats)
                if len(response_sorted) > 0:
                    LOGGER.info('Sort the list successful')
                    for current_list in response_sorted:
                        current_list_value = get_array_value(current_list)
                        if len(current_list_value) > 0:
                            type = current_list[0][TYPE]
                            if len(current_list_value) > 0:
                                cmd_sa_lock.acquire()
                                if type is MCC:
                                    cmd_sa[ID_MCC] = current_list_value
                                elif type is ACM:
                                    cmd_sa[ID_ACM] = current_list_value
                                elif type is ATS:
                                    cmd_sa[ID_ATS] = current_list_value
                                cmd_sa_lock.release()
                            else:
                                LOGGER.info('Get value of array failed')
                    response_clear_list = clear_all_list(list_dict_mcc, list_dict_acm, list_dict_ats)
                else:
                    LOGGER.info('Sort the list failed')
            time.sleep(period)
    except Exception as ex:
        LOGGER.error('Error at call function in thread shared_attributes_thread with message: %s', ex.message)


def classify_shared_attributes(key, value):
    formatted = {}
    try:
        if 'ats' in key:
            number = parse_ats_shared_attributes_to_number(key)
            if isinstance(number, int):
                formatted = {TYPE: 'ats', ID_SHARED_ATTRIBUTES: number, VALUE: value}
        elif 'mcc' in key:
            number = parse_mcc_shared_attributes_to_number(key)
            if isinstance(number, int):
                formatted = {TYPE: 'mcc', ID_SHARED_ATTRIBUTES: number, VALUE: value}
        elif 'acm' in key:
            number = parse_acm_shared_attributes_to_number(key)
            if isinstance(number, int):
                formatted = {TYPE: 'acm', ID_SHARED_ATTRIBUTES: number, VALUE: value}
    except Exception as ex:
        LOGGER.error('Error at classify_shared_attributes function with message: %s', ex.message)
    return formatted


def sort_list_dict(list_dict_mcc, list_dict_acm, list_dict_ats):
    new_list_mcc = []
    new_list_acm = []
    new_list_ats = []
    try:
        new_list_mcc = sorted(list_dict_mcc, key=itemgetter(ID_SHARED_ATTRIBUTES))
        new_list_acm = sorted(list_dict_acm, key=itemgetter(ID_SHARED_ATTRIBUTES))
        new_list_ats = sorted(list_dict_ats, key=itemgetter(ID_SHARED_ATTRIBUTES))
    except Exception as ex:
        LOGGER.error('Error at sort_list_dict function with message: %s', ex.message)
    return new_list_mcc, new_list_acm, new_list_ats


def classify_dict(response_classify):
    response = False
    try:
        if response_classify[TYPE] is 'mcc':
            list_dict_mcc.append(response_classify.copy())
            response = True
        elif response_classify[TYPE] is 'ats':
            list_dict_ats.append(response_classify.copy())
            response = True
        elif response_classify[TYPE] is 'acm':
            list_dict_acm.append(response_classify.copy())
            response = True
    except Exception as ex:
        LOGGER.error('Error at classify_dict function with message: %s', ex.message)
    return response


def get_array_value(list_sorted):
    list_value = []
    try:
        for x in list_sorted:
            list_value.append(x[VALUE])
    except Exception as ex:
        LOGGER.error('Error at get_array_value function with message: %s', ex.message)
    return list_value


def clear_all_list(list_dict_mcc, list_dict_acm, list_dict_ats):
    flag = False
    try:
        del list_dict_mcc[:]
        del list_dict_acm[:]
        del list_dict_ats[:]
        if len(list_dict_mcc) == 0 and len(list_dict_acm) == 0 and len(list_dict_ats) == 0:
            LOGGER.info('Clear all list successful')
            flag = True
        else:
            LOGGER.info('Fail while clear all list')
    except Exception as ex:
        LOGGER.error('Error at clear_all_list function with message: %s', ex.message)
    return flag
