from config import *
from config.common_lcd_services import *


# HungLQ
def get_title_rfid():
    try:
        show = [5, 'THONG TIN RFID']
        cmd_lcd[ROW_1] = str(show)
    except Exception as ex:
        LOGGER.error('Error at get_title_rfid function with message: %s', ex.message)


def get_info_rfid():
    try:
        json_file = open('./last_rfid_card_code.json', )
        rfid_info = json.load(json_file)
        status = 'Ket noi' if client_attributes.get('mccRfidConnectState') > 0 else 'Mat ket noi'
        cmd_lcd[ROW_2] = [5, str(status)]
        cmd_lcd[ROW_3] = [5, str(rfid_info['Time'])]
        cmd_lcd[ROW_4] = [5, str(rfid_info['StaffCode'])]
    except Exception as ex:
        LOGGER.error('Error at get_info_rfid function with message: %s', ex.message)


def get_screen_rfid():
    try:
        get_title_rfid()
        get_info_rfid()
    except Exception as ex:
        LOGGER.error('Error at get_screen_rfid function with message: %s', ex.message)
