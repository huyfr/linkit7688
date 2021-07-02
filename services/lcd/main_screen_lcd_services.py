import requests
from datetime import datetime
from config import *
from config.common import *
from config.common_lcd_services import *
from operate.led_thread import get_sate_led_alarm
from operate.rfid_thread import KEY_RFID
URL_NV = 'http://123.30.214.139:8517/api/services/app/DMNhanVienRaVaoTram/GetNhanVienRaVaoTram'


# HungLQ
class main_screen:
    def __init__(self):
        pass

    def get_temp_tram(self):
        try:
            warning = ''
            json_file = open('./last_temp.json', )
            temp = json.load(json_file)
            acmTempInOld = temp['acmTempIndoor']
            acmTempOutOld = temp['acmTempOutdoor']
            acmHumidInOld = temp['acmHumidIndoor']
            warningOld = temp['isWarning']
            acmTempIn = telemetries.get('acmTempIndoor')
            acmTempOut = telemetries.get('acmTempOutdoor')
            acmHumidIn = telemetries.get('acmHumidIndoor')
            check = get_sate_led_alarm(telemetries)
            warning = '!!!' if check == 0 else ''
            LOGGER.info('Warning: %s', warning)
            if (
                    acmTempInOld != acmTempIn or acmTempOutOld != acmTempOut or acmHumidInOld != acmHumidIn or warningOld != warning) and (
                    acmTempIn is not None and acmTempOut is not None and acmHumidIn is not None):
                Recheck = {"acmTempIndoor": acmTempIn, "acmTempOutdoor": acmTempOut, "acmHumidIndoor": acmHumidIn,
                           "isWarning": warning}
                self.write_to_json(Recheck, './last_temp.json')
                show = str(acmTempIn) + ' ' + str(acmTempOut) + ' ' + str(
                    acmHumidIn) + ' ' + warning + SALT_DOLLAR_SIGN + str(ROW_3) + END_CMD
                cmd_lcd[UPDATE_VALUE] = show
                LOGGER.info('acmTempIndoor, acmTempOutdoor, acmHumidIndoor: %s', show)
        except Exception as ex:
            LOGGER.error('Error at get_temp_tram function with message: %s', ex.message)


    def get_user_tram(self):
        try:
            if KEY_RFID in client_attributes:
                rfid_card = client_attributes.get(KEY_RFID)
                staffCode = rfid_card
                param = {'input': rfid_card}
                response = requests.get(url=URL_NV, params=param)
                if response.status_code == 200:
                    LOGGER.info('Send log request to Smartsite successful!')
                    staff = json.loads(response.content)['result']
                    if staff is not None:
                        staffCode = json.loads(response.content)['result']['maNhanVien']
                show = str(staffCode) + SALT_DOLLAR_SIGN + str(ROW_4) + END_CMD
                cmd_lcd[UPDATE_VALUE] = show
                dt_string = datetime.now().strftime("%d/%m/%Y %H:%M")
                rfid_info = {"Time": dt_string, "StaffCode": staffCode}
                self.write_to_json(rfid_info, './last_rfid_card_code.json')
                LOGGER.info('Ma nhan vien: %s', show)
        except Exception as ex:
            LOGGER.error('Error at get_user_tram function with message: %s', ex.message)


    def get_datetime_now(self):
        try:
            json_file = open('./last_time.json', )
            timeOld = json.load(json_file)
            timeNew = datetime.now().strftime("%M")
            if timeNew != timeOld:
                self.write_to_json(timeNew, './last_time.json')
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M")
                show = str(dt_string) + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD
                cmd_lcd[UPDATE_VALUE] = show
                LOGGER.info('DateTime now: %s', show)
        except Exception as ex:
            LOGGER.error('Error at get_datetime_now function with message: %s', ex.message)


    def get_title_main(self):
        try:
            show = 'MAKE IN MOBIFONE' + SALT_DOLLAR_SIGN + str(ROW_1) + END_CMD
            cmd_lcd[UPDATE_VALUE] = show
            LOGGER.info('Title: %s', show)
        except Exception as ex:
            LOGGER.error('Error at set_title_main function with message: %s', ex.message)


    def write_to_json(body, fileUrl):
        try:
            json_last_trace = json.dumps(body)
            with io.open(fileUrl, 'wb') as last_trace_file:
                last_trace_file.write(json_last_trace)
            LOGGER.info('Command information just send: %s', body)
        except Exception as ex:
            LOGGER.error('Error at write_to_json function with message: %s', ex.message)


# def get_screen_main():
#     try:
#         get_title_main()
#         while True:
#             get_user_tram()
#             get_temp_tram()
#             get_datetime_now()
#             time.sleep(3)
#     except Exception as ex:
#         LOGGER.error('Error at get_screen_main function with message: %s', ex.message)
