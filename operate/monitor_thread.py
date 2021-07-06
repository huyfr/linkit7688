import time

from config import *
from monitor import *


def call():
    period = 60
    while True:
        time.sleep(period)
        if shared_attributes.get('acmControlAuto', default_data.acmControlAuto):
            acm.check_status()
        # mcc.check_status()
        # Check if device is set in Auto mode
        # if shared_attributes.get('atsControlAuto', default_data.atsControlAuto):
        #     # then call its auto procedure
        #     ats.check_status()
        # Check if device is set in Auto mode
        # if 'acmControlAuto' in shared_attributes:
        #     acmAuto = shared_attributes['acmControlAuto']
        #     if acmAuto == 1:
        #         acm.check_status()
        # then call its auto procedure
