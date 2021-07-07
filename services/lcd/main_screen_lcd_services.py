import requests
from datetime import datetime
from config import *
from config.common import UPDATE_VALUE
from config.common_api import PREFIX, DOMAIN, API_GET_STAFF
from config.common_lcd_services import *
from operate.rfid_thread import KEY_RFID

timeOld = '61'
titleOld = ''
rfidOld = ''
acmTempInOld = ''
acmTempOutOld = ''
acmHumidInOld = ''
warningOld = ''
url_get_staff = PREFIX + DOMAIN + API_GET_STAFF


def write_to_json(body, fileUrl):
    try:
        json_last_trace = json.dumps(body)
        with io.open(fileUrl, 'wb') as last_trace_file:
            last_trace_file.write(json_last_trace)
        LOGGER.info('write to json success: %s', str(fileUrl))
    except Exception as ex:
        LOGGER.error('Error at write_to_json function with message: %s', ex.message)


# HungLq
def screen_main():
    try:
        get_title_main()
        get_datetime_now()
        get_temp_tram()
        get_user_tram()
    except Exception as ex:
        LOGGER.error('Error at call function in screen_main with message: %s', ex.message)


def read_to_json(fileUrl):
    try:
        json_file = open(fileUrl, )
        json_info = json.load(json_file)
    except Exception as ex:
        LOGGER.error('Error at call function in read_to_json with message: %s', ex.message)
    return json_info


def get_datetime_now():
    from control import process_cmd_lcd
    global timeOld
    try:
        timeNew = datetime.now().strftime("%M")
        if timeNew != timeOld:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M")
            show = str(dt_string)
            process_cmd_lcd(ROW_2, UPDATE_VALUE, show)
            LOGGER.info('MAIN SCREEN DATETIME NOW: %s', str(show))
            timeOld = timeNew
    except Exception as ex:
        LOGGER.error('Error at call function in check_key_code with message: %s', ex.message)


def get_title_main():
    from control import process_cmd_lcd
    # global titleOld
    try:
        # if titleOld == '':
        show = 'MAKE IN MOBIFONE'
        process_cmd_lcd(ROW_1, UPDATE_VALUE, show)
        # titleOld = 'MAKE IN MOBIFONE'
        LOGGER.info('MAIN SCREEN TITLE: %s', str(show))
    except Exception as ex:
        LOGGER.error('Error at set_title_main function with message: %s', ex.message)


def get_temp_tram():
    from control import process_cmd_lcd
    global acmTempInOld
    global acmTempOutOld
    global acmHumidInOld
    global warningOld
    try:
        warning = ''
        # tel = read_to_json('./latest_telemetry.json')
        tel = telemetries
        acmTempIn = tel.get('acmTempIndoor')
        acmTempOut = tel.get('acmTempOutdoor')
        acmHumidIn = tel.get('acmHumidIndoor')
        new_list = dict(filter(lambda elem: elem[0].lower().find('state') != -1, dct_alarm.items()))
        if len(new_list) > 0:
            check = any(elem != 0 for elem in new_list.values())
            warning = '!!!' if check else ''
        if (
                acmTempInOld != acmTempIn or acmTempOutOld != acmTempOut or acmHumidInOld != acmHumidIn or warningOld != warning) and (
                acmTempIn is not None and acmTempOut is not None and acmHumidIn is not None):
            acmTempInOld = acmTempIn
            acmTempOutOld = acmTempOut
            acmHumidInOld = acmHumidIn
            warningOld = warning
            show = str(acmTempIn) + ' ' + str(acmTempOut) + ' ' + str(
                acmHumidIn) + ' ' + warning
            process_cmd_lcd(ROW_3, UPDATE_VALUE, show)
            LOGGER.info('MAIN SCREEN TEMP AND ALARM NOW: %s', str(show))
    except Exception as ex:
        LOGGER.error('Error at get_temp_tram function with message: %s', ex.message)


def get_user_tram():
    from control import process_cmd_lcd
    try:
        # rfid = read_to_json('./latest_client_attributes.json')
        rfid = client_attributes
        if KEY_RFID in rfid:
            rfid_card = rfid.get(KEY_RFID)
            staffCode = rfid_card
            param = {'input': rfid_card}
            response = requests.get(url=url_get_staff, params=param)
            if response.status_code == 200:
                LOGGER.info('Send log request to Smartsite successful!')
                staff = json.loads(response.content)['result']
                if staff is not None:
                    staffCode = json.loads(response.content)['result']['maNhanVien']
            show = str(staffCode)
            process_cmd_lcd(ROW_4, UPDATE_VALUE, show)
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M")
            rfid_info = {"Time": dt_string, "StaffCode": staffCode}
            write_to_json(rfid_info, './last_rfid_card_code.json')
            LOGGER.info('MAIN SCREEN RFIDCODE OR STAFFCODE NOW: %s', str(show))
    except Exception as ex:
        LOGGER.error('Error at get_user_tram function with message: %s', ex.message)
