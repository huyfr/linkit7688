import io
import json
import logging
import threading

from . import default_data
import mqtt

with io.open('./config/devices.json', encoding='utf8') as f:
    device_config = json.load(f)
LOGGER = logging.getLogger('App')
BYTE_ORDER = 'little'
HOST = device_config['host']
ACCESS_TOKEN = device_config['access_token']
CLIENT_ID = device_config['device_id']
DEVICE_MCC = device_config['mcc']
DEVICE_ACM = device_config['acm']
DEVICE_ATS = device_config['ats']
CLIENT = mqtt.TBGatewayMqttClient(host=HOST, port=10883, token=ACCESS_TOKEN)
IO_PORT = '/dev/ttyS0'
# IO_PORT = 'COM3'
BAUDRATE = 115200
UPDATE_PERIOD = 7 * 24 * 60 * 60
# uncomment when test auto update firmware
UPDATE_PERIOD = 60
READ_PER_WRITE = 20
MAX_TRIES = 2

shared_attributes = {}
client_attributes = {}
update_attributes = {}
telemetries = {}
commands = {}
lcd_services = {}
cmd_led = {}
cmd_lcd = {}
# cmd_rfid = {}
cmd_sa = {}

update_attributes_lock = threading.Lock()
telemetries_lock = threading.Lock()
commands_lock = threading.Lock()
lcd_services_lock = threading.Lock()
cmd_led_lock = threading.Lock()
cmd_lcd_lock = threading.Lock()
# cmd_rfid_lock = threading.Lock()
cmd_sa_lock = threading.Lock()


