import json
import subprocess
import time

import requests

from config import LOGGER, CLIENT_ID
from config.common_api import *

COMMAND_RESET_SERVICE_7688 = '/etc/init.d/7688 stop && /etc/init.d/7688 start'
url_check_connection = PREFIX + DOMAIN + API_CHECK_CONNECTION
params = {'gatewayId': CLIENT_ID}


def call():
    period = 60
    while True:
        try:
            response = requests.get(url=url_check_connection, params=params)
            if response.status_code == 200:
                LOGGER.info('Send check connection request to Smartsite successful!')
                active = json.loads(response.content)['result']
                if active:
                    LOGGER.info('Gateway is online!')
                else:
                    LOGGER.info('Gateway is offline!')
                    subprocess.Popen(COMMAND_RESET_SERVICE_7688, shell=True, stdout=subprocess.PIPE)
            else:
                LOGGER.info('Response from Smartsite is not 200')
                subprocess.Popen(COMMAND_RESET_SERVICE_7688, shell=True, stdout=subprocess.PIPE)
        except Exception as ex:
            LOGGER.info('Error when check connection with message: %s', ex.message)
            subprocess.Popen(COMMAND_RESET_SERVICE_7688, shell=True, stdout=subprocess.PIPE)
        time.sleep(period)
