from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *


def get_title_ats():
    from control import process_cmd_lcd
    try:
        show = 'THONG TIN ATS'
        process_cmd_lcd(ROW_1, UPDATE_VALUE, show)
    except Exception as ex:
        LOGGER.error('Error at get_title_ats function with message: %s', ex.message)


def get_info_ats():
    from control import process_cmd_lcd
    try:
        infor_ats = client_attributes
        status = 'Ket noi' if infor_ats.get('atsConnect') > 0 else 'Mat ket noi'
        resource = 'Nguon: May phat' if infor_ats.get('atsContactorGenState') > 0 else 'Nguon: Dien luoi'
        mode = 'Che do: ' + str(telemetries.get('atsState'))
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(status))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(resource))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(mode))
    except Exception as ex:
        LOGGER.error('Error at get_info_ats function with message: %s', ex.message)


def get_detail_screen1_ats():
    row2 = ''
    row3 = ''
    row4 = ''
    from control import process_cmd_lcd
    try:
        row2 = 'Dien luoi: ' + str(telemetries.get('atsAcState'))
        row3 = 'May phat: ' + str(telemetries.get('atsGenState'))
        row4 = 'Che do M.Phat: ' + str(telemetries.get('atsState'))
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_detail_screen2_ats():
    row2 = ''
    row3 = ''
    row4 = ''
    from control import process_cmd_lcd
    try:
        row2 = str(telemetries.get('atsVacP1')) + 'V' + str(telemetries.get('atsVacP2')) + 'V' + str(
            telemetries.get('atsVacP3')) + 'V'
        row3 = str(telemetries.get('atsVgenP1')) + 'V' + str(telemetries.get('atsVgenP2')) + 'V' + str(
            telemetries.get('atsVgenP3')) + 'V'
        row4 = str(telemetries.get('atsVloadP1')) + 'V' + str(telemetries.get('atsVloadP2')) + 'V' + str(
            telemetries.get('atsVloadP3')) + 'V'
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_detail_screen3_ats():
    row2 = ''
    row3 = ''
    row4 = ''
    from control import process_cmd_lcd
    try:
        row2 = str(telemetries.get('atsIloadP1')) + 'A' + str(telemetries.get('atsIloadP2')) + 'A' + str(
            telemetries.get('atsIloadP3')) + 'A'
        row3 = str(telemetries.get('atsPac1')) + 'W' + str(telemetries.get('atsPac2')) + 'W' + str(
            telemetries.get('atsPac3')) + 'W'
        row4 = str(telemetries.get('atsVacFreq')) + 'Hz' + str(telemetries.get('atsVgenFreq')) + 'Hz' + str(
            telemetries.get('atsVloadFreq')) + 'Hz'
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_detail_screen4_ats():
    row2 = ''
    row3 = ''
    row4 = ''
    from control import process_cmd_lcd
    try:
        row2 = str(telemetries.get('mccDcBat1Temp')) + 'C' + str(telemetries.get('mccDcBat2Temp')) + 'C' + str(
            telemetries.get('mccDcBat3Temp')) + 'C'
        row3 = str(telemetries.get('mccDcV1')) + 'V' + str(telemetries.get('mccDcI1')) + 'A' + str(
            telemetries.get('mccDcP1')) + 'W'
        row4 = str(telemetries.get('mccDcV2')) + 'V' + str(telemetries.get('mccDcI2')) + 'A' + str(
            telemetries.get('mccDcP2')) + 'W'
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_detail_screen5_ats():
    row2 = ''
    row3 = ''
    row4 = ''
    from control import process_cmd_lcd
    try:
        row2 = str(telemetries.get('mccDcV3 ')) + 'V' + str(telemetries.get('mccDcI3')) + 'A' + str(
            telemetries.get('mccDcP3')) + 'W'
        row3 = str(telemetries.get('mccDcV4')) + 'V' + str(telemetries.get('mccDcI4')) + 'A' + str(
            telemetries.get('mccDcP4')) + 'W'
        row4 = str(telemetries.get('mccDcV5')) + 'V' + str(telemetries.get('mccDcI5')) + 'A' + str(
            telemetries.get('mccDcP5')) + 'W'
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_screen_ats():
    try:
        get_title_ats()
        get_info_ats()
    except Exception as ex:
        LOGGER.error('Error at get_screen_ats function with message: %s', ex.message)
