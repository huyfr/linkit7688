from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *

last_cmd_lcd = './last_cmd_screen.json'


def get_title_ats(row1):
    from control import process_cmd_lcd
    try:
        show = 'THONG TIN ATS'
        if row1 != show:
            process_cmd_lcd(ROW_1, UPDATE_VALUE, show)
            row1 = show
    except Exception as ex:
        LOGGER.warning('Error at get_title_ats function with message: %s', ex.message)
    return row1


def get_info_ats(row2_old, row3_old, row4_old):
    from control import process_cmd_lcd
    try:
        list_row = []
        row2 = 'Ket noi' if convert_to_string_default('atsConnect', 1) != '0' else 'Mat ket noi'
        row3 = 'Nguon: May phat' if convert_to_string_default('atsContactorGenState', 1) != '0' else 'Nguon: Dien luoi'
        row4 = 'Che do: ' + convert_to_string_default('atsState', 1)
        if row2_old != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            row2_old = row2
        if row3_old != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            row3_old = row3
        if row4_old != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            row4_old = row4
        LOGGER.info('ATS SCREEN : %s', 1)

        list_row.append(row2_old)
        list_row.append(row3_old)
        list_row.append(row4_old)
        return list_row
    except Exception as ex:
        LOGGER.warning('Error at get_info_ats function with message: %s', ex.message)


def get_detail_screen1_ats():
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json

    try:
        all_row = read_to_json(last_cmd_lcd)

        row2 = 'Dien luoi: ' + convert_to_string_default('atsAcState', 1)
        row3 = 'May phat: ' + convert_to_string_default('atsGenState', 1) + '(' + convert_to_string_default('atsGenRunningDuration', 1) + 'p)'
        row4 = 'Che do M.Phat: ' + convert_to_string_default('atsState', 1)
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            all_row['row4'] = row4

        write_to_json(all_row, last_cmd_lcd)
        LOGGER.debug('ATS SCREEN : %s', 2)
    except Exception as ex:
        LOGGER.warning('Error at get_detail_ats function with message: %s', ex.message)


def get_detail_screen2_ats():
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json
    try:
        all_row = read_to_json(last_cmd_lcd)

        row2 = convert_to_string_default('atsVacP1', 2) + 'V ' + convert_to_string_default('atsVacP2', 2) + 'V ' \
               + convert_to_string_default('atsVacP3', 2) + 'V'
        row3 = convert_to_string_default('atsVgenP1', 2) + 'V ' + convert_to_string_default('atsVgenP2', 2) + 'V ' \
               + convert_to_string_default('atsVgenP3', 2) + 'V'
        row4 = convert_to_string_default('atsVloadP1', 2) + 'V ' + convert_to_string_default('atsVloadP2', 2) + 'V ' \
               + convert_to_string_default('atsVloadP3', 2) + 'V'
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            all_row['row4'] = row4
        LOGGER.debug('ATS SCREEN : %s', 3)
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.warning('Error at get_detail_screen2_ats function with message: %s', ex.message)


def get_detail_screen3_ats():
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json
    try:
        all_row = read_to_json(last_cmd_lcd)
        row2 = convert_to_string_default('atsIloadP1', 3) + 'A ' + convert_to_string_default('atsIloadP2',
                                                                                 3) + 'A ' + convert_to_string_default(
            'atsIloadP3', 3) + 'A'
        row3 = convert_to_string_default('atsPac1', 3) + 'kW ' + convert_to_string_default('atsPac2',
                                                                              3) + 'kW ' + convert_to_string_default(
            'atsPac3', 3) + 'kW'

        row4 = convert_to_string_default('atsVacFreq', 2) + 'Hz ' + convert_to_string_default('atsVgenFreq',
                                                                                  2) + 'Hz ' + convert_to_string_default(
            'atsVloadFreq', 2) + 'Hz'
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            all_row['row4'] = row4
        LOGGER.debug('ATS SCREEN : %s', 4)
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.warning('Error at get_detail_screen3_ats function with message: %s', ex.message)


def get_detail_screen4_ats():
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json
    try:
        all_row = read_to_json(last_cmd_lcd)
        row2 = convert_to_string_default('mccDcBat1Temp', 2) + 'C ' + convert_to_string_default('mccDcBat2Temp',
                                                                                    2) + 'C ' + convert_to_string_default(
            'mccDcBat3Temp', 2) + 'C'
        row3 = convert_to_string_default('mccDcV1', 2) + 'V ' + convert_to_string_default('mccDcI1',
                                                                              3) + 'A ' + convert_to_string_default(
            'mccDcP1', 3) + 'kW'
        row4 = convert_to_string_default('mccDcV2', 2) + 'V ' + convert_to_string_default('mccDcI2',
                                                                              3) + 'A ' + convert_to_string_default(
            'mccDcP2', 3) + 'kW'
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            all_row['row4'] = row4
        LOGGER.debug('ATS SCREEN : %s', 5)
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.warning('Error at get_detail_screen4_ats function with message: %s', ex.message)


def get_detail_screen5_ats():
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json
    try:
        all_row = read_to_json(last_cmd_lcd)
        row2 = convert_to_string_default('mccDcV3', 2) + 'V ' + convert_to_string_default('mccDcI3',
                                                                              3) + 'A ' + convert_to_string_default(
            'mccDcP3', 3) + 'kW'
        row3 = convert_to_string_default('mccDcV4', 2) + 'V ' + convert_to_string_default('mccDcI4',
                                                                              3) + 'A ' + convert_to_string_default(
            'mccDcP4', 3) + 'kW'
        row4 = convert_to_string_default('mccDcV5', 2) + 'V ' + convert_to_string_default('mccDcI5',
                                                                              3) + 'A ' + convert_to_string_default(
            'mccDcP5', 3) + 'kW'
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            all_row['row4'] = row4
        LOGGER.debug('ATS SCREEN : %s', 6)
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.warning('Error at get_detail_screen5_ats function with message: %s', ex.message)


def get_screen_ats():
    from control.utils import read_to_json, write_to_json
    try:
        all_row = read_to_json(last_cmd_lcd)
        row1 = all_row['row1']
        row2 = all_row['row2']
        row3 = all_row['row3']
        row4 = all_row['row4']
        # enter func display
        row1 = get_title_ats(row1)
        list_row = get_info_ats(row2, row3, row4)
        # save to file
        all_row['row1'] = row1
        all_row['row2'] = list_row[0]
        all_row['row3'] = list_row[1]
        all_row['row4'] = list_row[2]
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.warning('Error at get_screen_ats function with message: %s', ex.message)


def convert_to_string_default(key_tel, type_check):
    try:
        if type_check == 1:
            if key_tel in telemetries:
                return str(telemetries[key_tel])
            else:
                return ''
        elif type_check == 2:
            if key_tel in telemetries:
                return str(telemetries[key_tel])
            else:
                return '0'
        elif type_check == 3:
            if key_tel in telemetries:
                return str(telemetries[key_tel] // 1000)
            else:
                return '0'
        else:
            return '0'
    except Exception as ex:
        LOGGER.warning('Error at convert_to_string_default function with message: %s', ex.message)