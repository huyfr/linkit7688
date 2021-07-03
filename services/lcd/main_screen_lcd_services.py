import requests
from datetime import datetime
from config import *
from config.common import *
from config.common_lcd_services import *
from operate.led_thread import get_sate_led_alarm
from operate.rfid_thread import KEY_RFID

URL_NV = 'http://123.30.214.139:8517/api/services/app/DMNhanVienRaVaoTram/GetNhanVienRaVaoTram'


def write_to_json(body, fileUrl):
    try:
        json_last_trace = json.dumps(body)
        with io.open(fileUrl, 'wb') as last_trace_file:
            last_trace_file.write(json_last_trace)
        LOGGER.info('write to json success: %s', str(fileUrl))
    except Exception as ex:
        LOGGER.error('Error at write_to_json function with message: %s', ex.message)


# HungLQ
class main_screen:
    def __init__(self):
        pass


    # def get_datetime_title_now(self):
    #     try:
    #         json_file = open('./main_screen.json', )
    #         json_info = json.load(json_file)
    #         timeOld = json_info["time"]
    #         timeNew = datetime.now().strftime("%M")
    #         if timeNew != timeOld:
    #             json_info.update({'time': timeNew})
    #             write_to_json(json_info, './main_screen.json')
    #             now = datetime.now()
    #             dt_string = now.strftime("%d/%m/%Y %H:%M")
    #             show = 'MAKE IN MOBIFONE' + SALT_DOLLAR_SIGN + str(ROW_1) + END_CMD + str(
    #                 dt_string) + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD
    #             cmd_lcd[UPDATE_VALUE] = show
    #             LOGGER.info('MAIN SCREEN DATETIME AND TITLE NOW: %s', str(show))
    #     except Exception as ex:
    #         LOGGER.error('Error at get_datetime_now function with message: %s', ex.message)

    def get_datetime_title_now(self):
        try:
            LOGGER.info('Enter get_datetime_title_now function')
            cmd_lcd[UPDATE_VALUE] = 'MAKE IN MOBIFONE'
            LOGGER.info('Exit get_datetime_title_now function')
        except Exception as ex:
            LOGGER.error('Error at get_datetime_now function with message: %s', ex.message)


    def get_temp_tram(self):
        try:
            warning = ''
            json_file = open('./main_screen.json', )
            json_info = json.load(json_file)
            acmTempInOld = json_info['acmTempIndoor']
            acmTempOutOld = json_info['acmTempOutdoor']
            acmHumidInOld = json_info['acmHumidIndoor']
            warningOld = json_info['isWarning']
            acmTempIn = telemetries.get('acmTempIndoor')
            acmTempOut = telemetries.get('acmTempOutdoor')
            acmHumidIn = telemetries.get('acmHumidIndoor')
            check = get_sate_led_alarm(telemetries)
            warning = '!!!' if check == 0 else ''
            if (acmTempInOld != acmTempIn or acmTempOutOld != acmTempOut or acmHumidInOld != acmHumidIn or warningOld != warning) and (
                    acmTempIn is not None and acmTempOut is not None and acmHumidIn is not None):
                json_info.update({'acmTempIndoor': acmTempIn})
                json_info.update({'acmTempOutdoor': acmTempOut})
                json_info.update({'acmHumidIndoor': acmHumidIn})
                json_info.update({'isWarning': warning})
                write_to_json(json_info, './main_screen.json')
                show = str(acmTempIn) + ' ' + str(acmTempOut) + ' ' + str(
                    acmHumidIn) + ' ' + warning + SALT_DOLLAR_SIGN + str(ROW_3) + END_CMD
                cmd_lcd[UPDATE_VALUE] = show
                LOGGER.info('MAIN SCREEN TEMP AND ALARM NOW: %s', str(show))
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
                write_to_json(rfid_info, './last_rfid_card_code.json')
                LOGGER.info('MAIN SCREEN RFIDCODE OR STAFFCODE NOW: %s', str(show))
        except Exception as ex:
            LOGGER.error('Error at get_user_tram function with message: %s', ex.message)
