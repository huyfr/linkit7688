import time

from config import *
from config.common import *


def call():
    period = shared_attributes.get('periodSendTelemetry', default_data.periodSendTelemetry)
    while True:
        if CLIENT.is_connected():
            telemetry = format_telemetry(telemetries)
            for key, value in telemetry.items():
                CLIENT.gw_send_telemetry(key, value)
            LOGGER.info('Sent telemetry data')
            telemetries_lock.acquire()
            telemetries.clear()
            telemetries_lock.release()
        time.sleep(period)


def format_telemetry(dict_telemetry):
    list_telemetry = {DEVICE_MDC_1: [{}], DEVICE_MCC_1: [{}], DEVICE_ATS_1: [{}], DEVICE_ACM_1: [{}]}
    telemetry_mdc_1 = {}
    telemetry_mcc_1 = {}
    telemetry_ats_1 = {}
    telemetry_acm_1 = {}
    data_from_stm32 = dict_telemetry

    for key, value in data_from_stm32.items():
        if 'crmu' in key:
            telemetry_mdc_1[key] = value
        elif 'ats' in key:
            telemetry_ats_1[key] = value
        elif 'airc' in key:
            telemetry_acm_1[key] = value
        else:
            telemetry_mcc_1[key] = value

    if telemetry_mdc_1:
        list_telemetry[DEVICE_MDC_1] = [telemetry_mdc_1]
    if telemetry_mcc_1:
        list_telemetry[DEVICE_MCC_1] = [telemetry_mcc_1]
    if telemetry_ats_1:
        list_telemetry[DEVICE_ATS_1] = [telemetry_ats_1]
    if telemetry_acm_1:
        list_telemetry[DEVICE_ACM_1] = [telemetry_acm_1]

    return list_telemetry


# def format_telemetry():
#     list_telemetry = {DEVICE_MISC: [{}], DEVICE_AIRC: [{}], DEVICE_ATS: [{}], DEVICE_ATU: [{}], DEVICE_DC: [{}]}
#     telemetry_misc = {}
#     telemetry_airc = {}
#     telemetry_ats = {}
#     telemetry_atu = {}
#     telemetry_dc = {}
#     data_from_stm32 = replica_telemetry()
#     for key, value in data_from_stm32.items():
#         if 'misc' in key:
#             telemetry_misc[key] = value
#         elif 'airc' in key:
#             telemetry_airc[key] = value
#         elif 'ats' in key:
#             telemetry_ats[key] = value
#         elif 'atu' in key:
#             telemetry_atu[key] = value
#         elif 'dc' in key:
#             telemetry_dc[key] = value
#
#     if telemetry_misc:
#         list_telemetry[DEVICE_MISC] = [telemetry_misc]
#     if telemetry_airc:
#         list_telemetry[DEVICE_AIRC] = [telemetry_airc]
#     if telemetry_ats:
#         list_telemetry[DEVICE_ATS] = [telemetry_ats]
#     if telemetry_atu:
#         list_telemetry[DEVICE_ATU] = [telemetry_atu]
#     if telemetry_dc:
#         list_telemetry[DEVICE_DC] = [telemetry_dc]
#
#     return list_telemetry
