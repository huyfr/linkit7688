from config import *
from config.common import *
from config.common_lcd_services import *


# HungLQ
class rfid_screen:
    def __init__(self):
        pass

    def get_title_rfid(self):
        try:
            show = 'THONG TIN RFID' + SALT_DOLLAR_SIGN + str(ROW_1) + END_CMD
            cmd_lcd[UPDATE_VALUE] = str(show)
            LOGGER.info('Title: %s', str(show))
        except Exception as ex:
            LOGGER.error('Error at get_title_rfid function with message: %s', ex.message)


    def get_info_rfid(self):
        try:
            json_file = open('./last_rfid_card_code.json', )
            rfid_info = json.load(json_file)
            status = 'Ket noi' if client_attributes.get('mccRfidConnectState') > 0 else 'Mat ket noi'
            show = status + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD + rfid_info['Time'] + SALT_DOLLAR_SIGN + str(ROW_3) + END_CMD + rfid_info[
                'StaffCode'] + SALT_DOLLAR_SIGN + str(ROW_4) + END_CMD
            cmd_lcd[UPDATE_VALUE] = str(show)
            LOGGER.info('Title: %s', str(show))
        except Exception as ex:
            LOGGER.error('Error at get_info_rfid function with message: %s', ex.message)


# def get_screen_rfid():
#     try:
#         get_title_rfid()
#         while True:
#             get_info_rfid()
#             time.sleep(3)
#     except Exception as ex:
#         LOGGER.error('Error at get_screen_rfid function with message: %s', ex.message)

