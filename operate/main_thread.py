import os
import sys
import threading
import time
import io
import json
import math
import subprocess

from config import *
from config.default_data import data_dict
from devices import clock
from . import subscription_thread, monitor_thread, io_thread, telemetry_thread, update_attributes_thread, ui_thread

semaphore = threading.Semaphore(0)


def _connect_callback(client, userdata, flags, rc, *extra_params):
    LOGGER.info('Connection successful')
    semaphore.release()


# def _on_receive_attributes_callback(key, result, exception):
#     if exception is None:
#         LOGGER.debug(result)
#         for key, value in result.get('shared', {}).items():
#             shared_attributes[key] = value
#         for key, value in result.get('client', {}).items():
#             client_attributes[key] = value
#     else:
#         LOGGER.error(exception)
#     semaphore.release()

# def _on_receive_attributes_callback(key, result, exception):
#     if exception is None:
#         LOGGER.debug(result)
#         if 'value' in result:
#             shared_attributes[key] = result["value"]
#             LOGGER.info('Shared attributes changes')
#             LOGGER.info(shared_attributes)
#     else:
#         LOGGER.error(exception)
#     semaphore.release()

def _on_receive_attributes_callback(content, exception):
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


def call():
    try:
        LOGGER.info('Start main thread')
        try:
            CLIENT.connect(callback=_connect_callback)
            semaphore.acquire()
        except Exception as e:
            LOGGER.info('Fail to connect to server')

        if CLIENT.is_connected():
            LOGGER.debug('Set IO time')
            # clock.set()
            LOGGER.debug('Get original attributes')
            device_name = data_dict["attribute_name"]
            for key, value in device_name.items():
                CLIENT.gw_request_shared_attributes(key, value, _on_receive_attributes_callback)
                semaphore.acquire()
        else:
            LOGGER.debug('Get current time')
            clock.extract()
        LOGGER.info('Start working threads')

        CLIENT.gw_connect_device("device_airc", "default")
        CLIENT.gw_connect_device("device_ats", "default")
        CLIENT.gw_connect_device("device_atu", "default")
        CLIENT.gw_connect_device("device_dc", "default")
        CLIENT.gw_connect_device("device_crmu", "default")
        CLIENT.gw_connect_device("device_misc", "default")

        CLIENT.gw_subscribe_to_all_attributes(callback=subscription_thread._attribute_change_callback)
        CLIENT.gw_set_server_side_rpc_request_handler(handler=subscription_thread._gw_rpc_callback)

        # thread_list = [io_thread, telemetry_thread, update_attributes_thread, monitor_thread, ui_thread]
        thread_list = [telemetry_thread, update_attributes_thread, monitor_thread, ui_thread]

        for i, thread in enumerate(thread_list):
            thread.name = thread.__name__
            thread_list[i] = _init_thread(thread)

        LOGGER.info('Start supervising cycle')

        period = shared_attributes.get('periodUpdate', default_data.periodUpdate)
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
                for key in default_data.data_dict:
                    for sub_key in default_data.data_dict[key]:
                        default_data.data_dict[key][sub_key] = default_data.__dict__[sub_key]
                with io.open('./config/data.tmp', 'w+', encoding='utf8') as f:
                    f.write(unicode(json.dumps(default_data.data_dict, ensure_ascii=True), 'utf8'))
                os.system('rm ./config/data.json && mv ./config/data.tmp ./config/data.json')
            except Exception as e:
                LOGGER.error('Cannot persist data, error %s', str(e))

            current_update_cycle = math.floor(time.time() / UPDATE_PERIOD)
            if current_update_cycle > original_update_cycle and CLIENT.is_connected():
                LOGGER.info('Update system, disconnect with server')
                CLIENT.disconnect()
                LOGGER.info('Retrieve update from server')
                try:
                    subprocess.check_call(
                        'cd /IoT && git clone https://github.com/MeryKitty/linkit7688 && mv ./linkit ./linkit_old && mv ./linkit7688 ./linkit',
                        stdout=subprocess.STDOUT, stderr=subprocess.STDOUT)
                    LOGGER.info('Successfully update the program, reboot the system')
                    CLIENT.disconnect()
                    os.system('reboot')
                except subprocess.CalledProcessError as e:
                    LOGGER.error('Cannot update repository, error %s', str(e))
            time.sleep(period)
    except KeyboardInterrupt:
        CLIENT.disconnect()
        sys.exit(1)
    except Exception as e:
        LOGGER.error('Fatal error %s, terminate immediately', str(e))
        CLIENT.disconnect()
        sys.exit(1)


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
