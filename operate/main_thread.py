import math
import os
import subprocess
import time
from logging import root

import requests

from config import *
from config.default_data import data_dict
from control.utils import validate_log_level
from devices import clock
from . import subscription_thread, monitor_thread, io_thread, telemetry_thread, update_attributes_thread, \
    shared_attributes_thread, rfid_thread, led_thread, lcd_thread, send_log_thread, update_t_acm_thread
from .update_attributes_thread import format_client_attributes, get_list_key

semaphore = threading.Semaphore(0)


def _connect_callback(client, userdata, flags, rc, *extra_params):
    LOGGER.info('Connection successful')
    semaphore.release()


def _on_receive_shared_attributes_callback(content, exception):
    if exception is None:
        LOGGER.debug(content)
        if 'values' in content:
            list_shared_attributes = content['values']
            if isinstance(list_shared_attributes, dict):
                for key, value in list_shared_attributes.items():
                    shared_attributes[key] = value
            LOGGER.info('Shared attributes changes')
            LOGGER.info(shared_attributes)
        elif 'value' in content:
            value = content['value']
            key = content['key']
            shared_attributes[key] = value
    else:
        LOGGER.error(exception)
        disconnect_thingsboard()
    semaphore.release()


def _on_receive_client_attributes_callback(content, exception):
    if exception is None:
        LOGGER.debug(content)
        if 'values' in content:
            list_client_attributes = content['values']
            if isinstance(list_client_attributes, dict):
                for key, value in list_client_attributes.items():
                    client_attributes[key] = value
            LOGGER.info('client attributes changes')
            LOGGER.info(client_attributes)
        elif 'value' in content:
            value = content['value']
            key = content['key']
            client_attributes[key] = value
    else:
        LOGGER.error(exception)
        disconnect_thingsboard()
    semaphore.release()


def call():
    try:
        LOGGER.info('Start main thread')

        init_connect(DEVICE_MCC, DEVICE_ATS, DEVICE_ACM)

        thread_list = [io_thread, update_attributes_thread, telemetry_thread, led_thread, shared_attributes_thread,
                       rfid_thread, monitor_thread, lcd_thread, send_log_thread, update_t_acm_thread]

        for i, thread in enumerate(thread_list):
            thread.name = thread.__name__
            thread_list[i] = _init_thread(thread)

        LOGGER.info('Start supervising cycle')

        period = shared_attributes.get('mccPeriodUpdate', default_data.mccPeriodUpdate)
        original_update_cycle = math.floor(time.time() / UPDATE_PERIOD)
        while True:
            # auto reconnect
            auto_reconnect_thingsboard()

            # init when thread died
            restart_thread(thread_list)

            # copy file
            clone_default_data()

            # change log level
            temp_level = shared_attributes.get('mccLogLevel', default_data.mccLogLevel)
            set_log_level(temp_level)

            # check update
            current_update_cycle = math.floor(time.time() / UPDATE_PERIOD)
            auto_update(current_update_cycle, original_update_cycle)

            time.sleep(period)
    except Exception as ex:
        LOGGER.error('Fatal error %s, terminate immediately', str(ex.message))
        disconnect_thingsboard()


def set_log_level(int_level):
    try:
        level = validate_log_level(int_level)
        root.setLevel(level)
    except Exception as ex:
        LOGGER.warning('Error at set_log_level function with message: %s', ex.message)


def auto_reconnect_thingsboard():
    try:
        if not CLIENT.is_connected():
            LOGGER.info('Disconnected from server, try reconnecting')
            init_connect(DEVICE_MCC, DEVICE_ATS, DEVICE_ACM)
        else:
            LOGGER.info('Gateway is connected!')
    except Exception as ex:
        LOGGER.error('Error at auto_reconnect_thingsboard function with message: %s', ex.message)


def clone_default_data():
    try:
        # TODO: Check copy file
        for key in default_data.data_dict:
            for sub_key in default_data.data_dict[key]:
                default_data.data_dict[key][sub_key] = default_data.__dict__[sub_key]
        with io.open('/IoT/linkit7688/config/data.tmp', 'w+', encoding='utf8') as f:
            f.write(unicode(json.dumps(default_data.data_dict, ensure_ascii=True), 'utf8'))
        os.system('rm /IoT/linkit7688/config/data.json && mv /IoT/linkit7688/config/data.tmp /IoT/linkit7688/config/data.json')
    except Exception as ex:
        LOGGER.error('Cannot persist data, error %s', ex.message)


def restart_thread(thread_list):
    try:
        for i, thread in enumerate(thread_list):
            if not thread.isAlive():
                LOGGER.debug('Thread %s died, restarting', thread.getName())
                thread_list[i] = _init_thread(thread)
    except Exception as ex:
        LOGGER.debug('Error at restart_thread function with message: %s', ex.message)


def auto_update(current_update_cycle, original_update_cycle):
    latest_version = -1
    try:
        link_update = shared_attributes.get('mccLinkUpdate', default_data.mccLinkUpdate)
        link_version = shared_attributes.get('mccLinkVersion', default_data.mccLinkVersion)
        folder_name = link_update.split('/')[-1].split('.')[0]
        if current_update_cycle > original_update_cycle and CLIENT.is_connected():
            if link_version is not '':
                response_get_version = requests.get(link_version)
                if response_get_version.status_code == 200:
                    latest_version = json.loads(response_get_version.content)['version']
        version_file = open('./version.json', )
        current_version = json.load(version_file)['version']
        if latest_version > 0 and current_version > 0:
            if latest_version > current_version:
                LOGGER.info('Get new version: %s from server: %s', str(latest_version), link_version)
                LOGGER.info('Update system, disconnect with server')
                command = 'cd /IoT && ./update.sh ' + link_update + ' ' + folder_name
                subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            else:
                LOGGER.info('Current version is the latest')
    except Exception as ex:
        LOGGER.error('Cannot update repository, error %s', ex.message)


def disconnect_thingsboard():
    CLIENT.disconnect()
    LOGGER.info('Disconnect 3 devices and client successful!')


def init_connect(mcc, ats, acm):
    try:
        CLIENT.connect(callback=_connect_callback)
        semaphore.acquire()

        if CLIENT.is_connected():
            LOGGER.debug('Set IO time')
            clock.set()
            # shared_attributes
            device_shared_attributes_name = format_client_attributes(data_dict['shared'])
            for key, value in device_shared_attributes_name.items():
                list_shared_keys = get_list_key(value)
                CLIENT.gw_request_shared_attributes(key, list_shared_keys, _on_receive_shared_attributes_callback)
                semaphore.acquire()

            # client_attributes
            device_client_attributes_name = format_client_attributes(data_dict['client'])
            for key, value in device_client_attributes_name.items():
                list_client_keys = get_list_key(value)
                CLIENT.gw_request_client_attributes(key, list_client_keys, _on_receive_client_attributes_callback)
                semaphore.acquire()
        else:
            LOGGER.debug('Get current time')
            clock.extract()

        CLIENT.gw_connect_device(mcc, "default")
        CLIENT.gw_connect_device(ats, "default")
        CLIENT.gw_connect_device(acm, "default")
        CLIENT.gw_subscribe_to_all_attributes(callback=subscription_thread._attribute_change_callback)
        CLIENT.gw_set_server_side_rpc_request_handler(handler=subscription_thread._gw_rpc_callback)
        LOGGER.info('Init connection completed')
    except Exception as ex:
        LOGGER.error('Error at init_connect function with message: %s', ex.message)


def _init_thread(target):
    thread = threading.Thread(target=target.call)
    thread.setName(target.name)
    thread.setDaemon(True)
    thread.call = target.call
    try:
        thread.start()
        LOGGER.debug('Start thread %s successfully', thread.getName())
    except Exception as ex:
        LOGGER.debug('Fail to start thread %s with message: %s', thread.getName(), ex.message)
    return thread
