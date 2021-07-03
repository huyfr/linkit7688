import time

from config import *
from monitor import *


def call():
    period = 60
    while True:
        LOGGER.info('Enter monitor thread. This is log for test')
        # mcc.check_status()
        # Check if device is set in Auto mode
        # if shared_attributes.get('atsControlAuto', default_data.atsControlAuto):
        #     # then call its auto procedure
        #     ats.check_status()
        # Check if device is set in Auto mode
        # if shared_attributes.get('acmControlAuto', default_data.acmControlAuto):
            # then call its auto procedure
            # acm.check_status()
        time.sleep(period)
