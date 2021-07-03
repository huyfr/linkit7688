import time

from datetime import datetime
from config import *
from config.common import *
from config.common_lcd_services import *

BAN_TIN_CANH_BAO = 'BAN TIN CANH BAO'


class alarm_lcd_service:

    def __init__(self):
        pass

    def init_show_alarm(self):
        try:
            cmd_lcd[UPDATE_VALUE] = self.create_cmd_multi(self.BAN_TIN_CANH_BAO, ROW_1)
            # LOGGER.info('List telemitries: %s', telemetries)
            while True:
                if telemetries:
                    self.check_alarm(tel_lcd=telemetries)
                time.sleep(3)
        except Exception as ex:
            LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)

    def check_alarm(self, tel_lcd):
        cmd_lcd_dict = {}
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        try:
            max_tem = shared_attributes.get('acmExpectedTemp', default_data.acmExpectedTemp)
            LOGGER.info('MAX TEMPERATURE: %s', str(max_tem))
            if tel_lcd:
                if tel_lcd.get('mccFireState') == 1:
                    self.create_for_each('CB Chay!', dt_string)
                elif tel_lcd.get('mccSmokeState') == 1:
                    self.create_for_each('CB Khoi!', dt_string)
                elif tel_lcd.get('acmTempIndoor') > max_tem:
                    self.create_for_each('CB Nhiet!', dt_string)
                elif tel_lcd.get('mccFloodState') == 1:
                    self.create_for_each('CB Ngap!', dt_string)
                elif tel_lcd.get('mccDoorState') == 1:
                    self.create_for_each('CB Cua!', dt_string)
                else:
                    self.create_for_each('An Toan!', '')

        except Exception as ex:
            LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)
        return cmd_lcd_dict

    def create_for_each(self, string1, string2):
        try:
            el1 = self.create_cmd_multi(string1, ROW_2)
            el1 += self.create_cmd_multi(string2, ROW_3)
            LOGGER.info('CANH BAO : %s', el1)
            cmd_lcd[UPDATE_VALUE] = el1
        except Exception as ex:
            LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)

    def create_cmd_multi(self, string, row):
        return str(string) + SALT_DOLLAR_SIGN + str(row) + END_CMD