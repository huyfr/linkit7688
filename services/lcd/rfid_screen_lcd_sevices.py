from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *


# HungLQ
def get_title_rfid():
    from control import process_cmd_lcd
    try:
        show = 'THONG TIN RFID'
        process_cmd_lcd(ROW_1, UPDATE_VALUE, show)
    except Exception as ex:
        LOGGER.error('Error at get_title_rfid function with message: %s', ex.message)


def get_info_rfid():
    from control import process_cmd_lcd
    try:
        json_file = open('./last_rfid_card_code.json', )
        rfid_info = json.load(json_file)
        status = 'Ket noi' if client_attributes.get('mccRfidConnectState') > 0 else 'Mat ket noi'
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(status))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(rfid_info['Time']))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(rfid_info['StaffCode']))
    except Exception as ex:
        LOGGER.error('Error at get_info_rfid function with message: %s', ex.message)


def get_screen_rfid():
    try:
        get_title_rfid()
        get_info_rfid()
    except Exception as ex:
        LOGGER.error('Error at get_screen_rfid function with message: %s', ex.message)
