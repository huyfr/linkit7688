import os
import time

import requests

from config import LOGGER, device_config, shared_attributes, default_data
from config.common_api import API_SEND_LOG, PREFIX, DOMAIN
from control.utils import read_to_json, write_to_json

TIME_PERIOD = 90
LOG_PATH = './app.log.1'
DESTINATION = './log'
LAST_UPDATE_LOG_PATH = './last_update_log.json'
SUCCESS = 1
url_send_log = PREFIX + DOMAIN + API_SEND_LOG


def call():
    period = TIME_PERIOD
    try:
        while True:
            time.sleep(period)
            existence = check_log_exist(LOG_PATH)
            if not existence:
                continue

            detected = detect_new_log(LAST_UPDATE_LOG_PATH, LOG_PATH)
            if not detected[0]:
                continue

            body = write_body_send_log(LOG_PATH)
            allow_upload = shared_attributes.get('mccUploadLog', default_data.mccUploadLog)
            if len(body) > 0 and allow_upload:
                response = send_log_smartsite(body[0], body[-1])
                if not response:
                    continue

                dct_log_file = compose_file(detected[1], SUCCESS)
                if len(dct_log_file) > 0:
                    write_to_json(dct_log_file, LAST_UPDATE_LOG_PATH)
    except Exception as ex:
        LOGGER.warning('Error at call function in send_log_thread with message: %s', ex.message)


def check_log_exist(path):
    result = False
    try:
        if os.path.exists(path):
            result = True
            LOGGER.debug('app.log.1 file exists')
        else:
            LOGGER.debug('app.log.1 file does not exist')
    except Exception as ex:
        LOGGER.warning('Error at check_log_exist function with message: %s', ex.message)
    return result


def detect_new_log(last_update_log_path, log_path):
    result = False
    last_modified = 0
    try:
        last_update_file = read_to_json(last_update_log_path)
        last_updated_date = last_update_file['updateDate']
        updated_date = os.path.getmtime(log_path)
        if updated_date > last_updated_date:
            result = True
            last_modified = updated_date
            LOGGER.debug('Backup log file has just been updated')
        else:
            LOGGER.debug('No change detected')
    except Exception as ex:
        LOGGER.warning('Error at detect_new_log function with message: %s', ex.message)
    return result, last_modified


def write_body_send_log(path_file):
    files = {}
    data = {}
    try:
        gateway_id = device_config['device_id']
        data = {'idTram': gateway_id}
        files = {"file": open(path_file, 'rb')}
    except Exception as ex:
        LOGGER.warning('Error at write_body_send_log function with message: %s', ex.message)
    return data, files


def send_log_smartsite(data, files):
    result = False
    try:
        if isinstance(data, dict) and isinstance(files, dict):
            if len(data) > 0 and len(files) > 0:
                response = requests.post(url_send_log, data=data, files=files)
                if response.status_code == 200:
                    result = True
                    LOGGER.debug('Send log to Smartsite successful!')
                else:
                    LOGGER.debug('Fail while send log to Smartsite. Status code is: %s', str(response.status_code))
        else:
            LOGGER.debug('Body is not dictionary!')
    except Exception as ex:
        LOGGER.warning('Error at send_log_smartsite function with message: %s', ex.message)
    return result


def compose_file(updated_date, status):
    dct_log = {}
    try:
        dct_log['updateDate'] = updated_date
        dct_log['status'] = status
    except Exception as ex:
        LOGGER.warning('Error at compose_file function with message: %s', ex.message)
    return dct_log

