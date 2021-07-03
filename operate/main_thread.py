import os
import time
import math
import subprocess

import requests

from config import *
from config.default_data import data_dict
from devices import clock
from . import subscription_thread, monitor_thread, io_thread, telemetry_thread, update_attributes_thread, ui_thread, \
    shared_attributes_thread, rfid_thread, led_thread, lcd_thread, check_connection_thread
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
    semaphore.release()


def call():
    try:
        LOGGER.info('Start main thread')
        try:
            CLIENT.connect(callback=_connect_callback)
            semaphore.acquire()
        except Exception as ex:
            LOGGER.info('Fail to connect to server with message: %s', ex.message)

        if CLIENT.is_connected():
            LOGGER.debug('Set IO time')
            clock.set()
            LOGGER.debug('Get original attributes')
            #shared_attributes
            device_shared_attributes_name = format_client_attributes(data_dict['shared'])
            for key, value in device_shared_attributes_name.items():
                list_shared_keys = get_list_key(value)
                CLIENT.gw_request_shared_attributes(key, list_shared_keys, _on_receive_shared_attributes_callback)
                semaphore.acquire()

            #client_attributes
            device_client_attributes_name = format_client_attributes(data_dict['client'])
            for key, value in device_client_attributes_name.items():
                list_client_keys = get_list_key(value)
                CLIENT.gw_request_client_attributes(key, list_client_keys, _on_receive_client_attributes_callback)
                semaphore.acquire()
        else:
            LOGGER.debug('Get current time')
            clock.extract()
        LOGGER.info('Start working threads')

        CLIENT.gw_connect_device(DEVICE_MCC, "default")
        CLIENT.gw_connect_device(DEVICE_ATS, "default")
        CLIENT.gw_connect_device(DEVICE_ACM, "default")

        CLIENT.gw_subscribe_to_all_attributes(callback=subscription_thread._attribute_change_callback)
        CLIENT.gw_set_server_side_rpc_request_handler(handler=subscription_thread._gw_rpc_callback)

        thread_list = [io_thread, update_attributes_thread, telemetry_thread, led_thread, lcd_thread, shared_attributes_thread, rfid_thread, monitor_thread, check_connection_thread]

        # enable when test in IDE
        # thread_list = [update_attributes_thread, telemetry_thread, led_thread, lcd_thread, shared_attributes_thread, rfid_thread, monitor_thread]

        for i, thread in enumerate(thread_list):
            thread.name = thread.__name__
            thread_list[i] = _init_thread(thread)

        LOGGER.info('Start supervising cycle')

        period = shared_attributes.get('mccPeriodUpdate', default_data.mccPeriodUpdate)
        original_update_cycle = math.floor(time.time() / UPDATE_PERIOD)
        while True:
            if not CLIENT.is_connected():
                LOGGER.info('Disconnected from server, try reconnecting')
                try:
                    CLIENT.connect(callback=_connect_callback)
                    semaphore.acquire()
                except:
                    LOGGER.info('Fail to connect to server')

            for i, thread in enumerate(thread_list):
                if not thread.isAlive():
                    LOGGER.debug('Thread %s died, restarting', thread.getName())
                    thread_list[i] = _init_thread(thread)

            try:
                # TODO: Check copy file
                for key in default_data.data_dict:
                    for sub_key in default_data.data_dict[key]:
                        default_data.data_dict[key][sub_key] = default_data.__dict__[sub_key]
                with io.open('/IoT/linkit7688/config/data.tmp', 'w+', encoding='utf8') as f:
                    f.write(unicode(json.dumps(default_data.data_dict, ensure_ascii=True), 'utf8'))
                os.system('rm /IoT/linkit7688/config/data.json && mv /IoT/linkit7688/config/data.tmp /IoT/linkit7688/config/data.json')
            except Exception as e:
                LOGGER.error('Cannot persist data, error %s', str(e))

            current_update_cycle = math.floor(time.time() / UPDATE_PERIOD)
            if current_update_cycle > original_update_cycle and CLIENT.is_connected():
                latest_version = -1
                try:
                    link_update = shared_attributes['mccLinkUpdate']
                    link_version = shared_attributes['mccLinkVersion']
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
                            command = 'cd /IoT && ./update.sh'
                            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                        else:
                            pass
                except Exception as ex:
                    LOGGER.error('Cannot update repository, error %s', ex.message)
            time.sleep(period)
    except KeyboardInterrupt:
        CLIENT.gw_disconnect_device(DEVICE_MCC)
        CLIENT.gw_disconnect_device(DEVICE_ATS)
        CLIENT.gw_disconnect_device(DEVICE_ACM)
        CLIENT.disconnect()
    except Exception as e:
        LOGGER.error('Fatal error %s, terminate immediately', str(e))
        CLIENT.gw_disconnect_device(DEVICE_MCC)
        CLIENT.gw_disconnect_device(DEVICE_ATS)
        CLIENT.gw_disconnect_device(DEVICE_ACM)
        CLIENT.disconnect()


def _init_thread(target):
    thread = threading.Thread(target=target.call)
    thread.setName(target.name)
    thread.setDaemon(True)
    thread.call = target.call
    try:
        thread.start()
        LOGGER.debug('Start thread %s successfully', thread.getName())
    except:
        LOGGER.debug('Fail to start thread %s', thread.getName())
    return thread
