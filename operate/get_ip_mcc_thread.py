import time

import netifaces

from config import LOGGER

PERIOD_GET_IP = 600


def call():
    period = PERIOD_GET_IP
    while True:
        try:
            default_gateway = get_ip_gateway()
            time.sleep(period)
        except Exception as ex:
            LOGGER.error('Error at call function in get_ip_mcc_thread with message: %s', ex.message)


def get_ip_gateway():
    try:
        gws = netifaces.gateways()
        LOGGER.info('Information gateway: %s', gws)
        return gws
    except Exception as ex:
        LOGGER.error('Error at get_ip_gateway function with message: %s', ex.message)

