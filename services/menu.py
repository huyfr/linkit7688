"""---------------------------------------------------------------------------------------------------------------------
                                                    Include
   ------------------------------------------------------------------------------------------------------------------"""
from config.common import *
from services.lcd import main_screen_lcd_services, ats_screen_lcd_services, ats_setting_lcd_service, \
    rfid_screen_lcd_sevices, rfid_setting_lcd_service, setting_info_screen_lcd_services, \
    setting_datetime_screen_lcd_services, setting_acm_screen_lcd_services
from services.lcd.acm_sreen_lcd_services import show_temp_condition, show_time_condition
from services.lcd.alarm_lcd_services import check_alarm
from services.lcd.ats_setting_lcd_service import reset_params as ats_reset_params
from services.lcd.main_screen_lcd_services import reset_params_main_display
from services.lcd.rfid_setting_lcd_service import reset_params as rfid_reset_params
from services.lcd.sensor_screen_lcd_services import *
# SonTH
from services.lcd.setting_screen_lcd_services import *


"""---------------------------------------------------------------------------------------------------------------------
                                                    Define 
   ------------------------------------------------------------------------------------------------------------------"""
ROW = [ROW_1, ROW_2, ROW_3, ROW_4]
TIME_OUT = 600

setting_display_print = {
    0: {
        'row1': 'CAI DAT HE THONG',
        'row2': '> Thong tin',
        'row3': 'Ngay gio',
        'row4': 'Thong so mang'
        },
    1: {
        'row1': 'CAI DAT HE THONG',
        'row2': 'Thong tin',
        'row3': '> Ngay gio',
        'row4': 'Thong so mang'
        },
    2: {
        'row1': 'CAI DAT HE THONG',
        'row2': 'Thong tin',
        'row3': 'Ngay gio',
        'row4': '> Thong so mang'
        },
    3: {
        'row1': 'CAI DAT HE THONG',
        'row2': '> Canh bao',
        'row3': 'Thiet bi ATS',
        'row4': 'Thiet bi RFID'
        },
    4: {
        'row1': 'CAI DAT HE THONG',
        'row2': 'Canh bao',
        'row3': '> Thiet bi ATS',
        'row4': 'Thiet bi RFID'
        },
    5: {
        'row1': 'CAI DAT HE THONG',
        'row2': 'Canh bao',
        'row3': 'Thiet bi ATS',
        'row4': '> Thiet bi RFID'
        },
    6: {
        'row1': 'CAI DAT HE THONG',
        'row2': '> Dieu hoa',
        'row3': '',
        'row4': ''
        }
}


"""---------------------------------------------------------------------------------------------------------------------
                                                Global variable
   ------------------------------------------------------------------------------------------------------------------"""
event = 0
ats_screen_index = 0
setting_screen_index = 0
last_setting_screen_index = -1
screen_lv1_index = 0
last_screen_lv1_index = -1
start_time = 0
time_count = 0
cycle_flag = False
time_setting_screen_index = 0
last_time_setting_screen_index = -1
last_cmd_lcd = './last_cmd_screen.json'
security_screen_index = 0
air_cond_screen_index = 0
go_sub_setting_flag = False
start_flag = True

"""---------------------------------------------------------------------------------------------------------------------
                                                Internal function
   ------------------------------------------------------------------------------------------------------------------"""
''' print lcd function '''


def clear_display():
    from control import process_cmd_lcd
    process_cmd_lcd(ROW_1, CLEAR, '')


def print_lcd(str1, str2, str3, str4):
    from control import process_cmd_lcd
    try:
        string = [str1, str2, str3, str4]
        LOGGER.debug('Send message print_lcd on lcd')
        i = 0
        while i < 4:
            if string[i] == '':
                string[i] = ' '
            status = process_cmd_lcd(ROW[i], UPDATE_VALUE, string[i])
            if status:
                i += 1
    except Exception as ex:
        LOGGER.warning('print_lcd function error: %s', ex.message)


def remove_json_file():
    try:
        file_json = read_to_json(last_cmd_lcd)
        file_json['row1'] = ""
        file_json['row2'] = ""
        file_json['row3'] = ""
        file_json['row4'] = ""
        write_to_json(file_json, last_cmd_lcd)
    except Exception as ex:
        LOGGER.warning('Error at remove_json_file_alarm function with message: %s', ex.message)


def read_to_json(file_url):
    try:
        json_file = open(file_url, )
        json_info = json.load(json_file)
        return json_info
    except Exception as ex:
        LOGGER.warning('Error at call function in read_to_json with message: %s', ex.message)


''' screen level 1 implement '''


def main_display():
    main_screen_lcd_services.screen_main()


def warning_display():
    check_alarm()


def security_sensor_info_display():
    LOGGER.debug('Enter security_sensor_info_display function')
    global event, security_screen_index

    if event == LEFT:
        security_screen_index = 0
    elif event == RIGHT:
        security_screen_index = 1
    if security_screen_index == 0:
        security_sensor_screen_1(telemetries)
    elif security_screen_index == 1:
        security_sensor_screen_2(telemetries)


def air_info_display():
    LOGGER.debug('Enter air_info_display function')
    global event, air_cond_screen_index

    if event == LEFT:
        air_cond_screen_index = 0
    elif event == RIGHT:
        air_cond_screen_index = 1
    if air_cond_screen_index == 0:
        show_temp_condition(telemetries)
    elif air_cond_screen_index == 1:
        show_time_condition(telemetries)


def ats_display():
    global ats_screen_index
    ats_display_func = {
        0: ats_screen_lcd_services.get_screen_ats,
        1: ats_screen_lcd_services.get_detail_screen1_ats,
        2: ats_screen_lcd_services.get_detail_screen2_ats,
        3: ats_screen_lcd_services.get_detail_screen3_ats,
        4: ats_screen_lcd_services.get_detail_screen4_ats,
        5: ats_screen_lcd_services.get_detail_screen5_ats
    }
    try:
        if event == RIGHT:
            ats_screen_index += 1
        elif event == LEFT:
            ats_screen_index -= 1
        if ats_screen_index > 5:
            ats_screen_index = 5
        elif ats_screen_index < 0:
            ats_screen_index = 0

        func = ats_display_func[ats_screen_index]
        # LOGGER.debug('ATS DISPLAY DETAIL %s', str(ats_screen_index))
        return func()
    except Exception as ex:
        LOGGER.warning('ats_display function error: %s', ex.message)


def rfid_display():
    rfid_screen_lcd_sevices.get_screen_rfid()
    LOGGER.debug('RFID DISPLAY')


def setting_display():
    global setting_screen_index, event, last_setting_screen_index, go_sub_setting_flag
    try:
        if not go_sub_setting_flag:
            if event == OK:
                go_sub_setting_flag = True
            elif event == UP:
                setting_screen_index -= 1
            elif event == DOWN:
                setting_screen_index += 1
            if event == LEFT:
                setting_screen_index -= 3
                if setting_screen_index < 3:
                    setting_screen_index = 0
                elif 6 > setting_screen_index >= 3:
                    setting_screen_index = 3
                elif setting_screen_index >= 6:
                    setting_screen_index = 6
            elif event == RIGHT:
                setting_screen_index += 3
                if setting_screen_index < 3:
                    setting_screen_index = 0
                elif 6 > setting_screen_index >= 3:
                    setting_screen_index = 3
                elif setting_screen_index >= 6:
                    setting_screen_index = 6
            if setting_screen_index > 6:
                setting_screen_index = 6
            elif setting_screen_index < 0:
                setting_screen_index = 0

            if last_setting_screen_index != setting_screen_index and not go_sub_setting_flag:
                print_lcd(setting_display_print[setting_screen_index]['row1'],
                          setting_display_print[setting_screen_index]['row2'],
                          setting_display_print[setting_screen_index]['row3'],
                          setting_display_print[setting_screen_index]['row4'])
                last_setting_screen_index = setting_screen_index
        if go_sub_setting_flag:
            select_setting()
        LOGGER.debug('setting_display, setting_screen_index: %s', str(setting_screen_index))
    except Exception as ex:
        LOGGER.warning('setting_display function error: %s', ex.message)


''' Setting implement '''


def select_setting():
    global event, setting_screen_index
    setting_function_list = {
        0: information_setting,
        1: time_setting,
        2: internet_setting,
        3: warning_setting,
        4: ats_setting,
        5: rfid_setting,
        6: acm_setting,
    }

    func = setting_function_list.get(setting_screen_index)
    return func()


def information_setting():
    global event, go_sub_setting_flag
    LOGGER.debug('Finish cai_dat_thong_tin function')
    if event == 0:
        return
    if setting_info_screen_lcd_services.info_setting_process(event):
        back_screen_setting()
        setting_info_screen_lcd_services.get_default_value()


def time_setting():
    from services.lcd.setting_datetime_screen_lcd_services import GO_CONFIRM
    global event, go_sub_setting_flag, last_setting_screen_index, setting_screen_index

    if event == 0:
        return
    if setting_datetime_screen_lcd_services.datetime_setting(event) is GO_CONFIRM:
        back_screen_setting()


def internet_setting():
    global event, setting_screen_index
    LOGGER.debug('event in internet_setting: %s', str(event))
    if event == 0:
        return
    LOGGER.debug('Enter internet_setting function, setting_screen_index: %s', str(setting_screen_index))
    # Call function xu ly keycode
    choose_config(setting_screen_index + 1)
    listen_key_code(event)


def warning_setting():
    global event, setting_screen_index
    if event == 0:
        return
    LOGGER.debug('Enter warning_setting function, setting_screen_index: %s', str(setting_screen_index))
    # Call function xu ly keycode
    choose_config(setting_screen_index + 1)
    listen_key_code(event)


def ats_setting():
    global event

    ats_setting_lcd_service.listen_key_code(event)


def rfid_setting():
    global event

    rfid_setting_lcd_service.listen_key_code(event)


def acm_setting():
    global event

    if event == 0:
        return
    if setting_acm_screen_lcd_services.acm_setting(event) == setting_acm_screen_lcd_services.GO_CONFIRM:
        back_screen_setting()
        setting_acm_screen_lcd_services.acm_setting_set_default_value()


def back_main_screen(button):
    from control import process_cmd_lcd
    global cycle_flag, time_count, screen_lv1_index, start_time

    try:
        if button != -1:
            start_time = time.time()
            cycle_flag = True
        else:
            return
        if cycle_flag is True:
            if (time.time() - start_time) >= (time_count + 1):
                time_count = time.time() - start_time
                LOGGER.debug('Time out come back to main display: %ds', time_count)
        if time_count > TIME_OUT:
            time_count = 0
            cycle_flag = False
            screen_lv1_index = ESC
            process_cmd_lcd(ROW_1, CLEAR, '')
            process_cmd_lcd(ROW_2, CLEAR, '')
            process_cmd_lcd(ROW_3, CLEAR, '')
            process_cmd_lcd(ROW_4, CLEAR, '')
    except Exception as ex:
        LOGGER.warning('back_main_screen function error: %s', ex.message)


def clear_event():
    global event

    event = 0


def move_default_var():
    global event, security_screen_index, ats_screen_index, last_setting_screen_index, last_screen_lv1_index, \
        last_time_setting_screen_index, go_sub_setting_flag, air_cond_screen_index

    security_screen_index = 0
    air_cond_screen_index = 0
    ats_screen_index = 0
    last_setting_screen_index = -1
    last_screen_lv1_index = -1
    last_time_setting_screen_index = -1
    go_sub_setting_flag = False


def back_screen_setting():
    global go_sub_setting_flag, last_setting_screen_index, setting_screen_index

    go_sub_setting_flag = False
    last_setting_screen_index = -1
    setting_screen_index = 0


"""---------------------------------------------------------------------------------------------------------------------
                                                 External function
   ------------------------------------------------------------------------------------------------------------------"""


def main_menu(button):
    global screen_lv1_index, event, last_screen_lv1_index, security_screen_index, ats_screen_index,\
        start_flag, setting_screen_index

    try:
        menu_function_list = {
            ESC: main_display,
            CANH_BAO: warning_display,
            CAM_BIEN: security_sensor_info_display,
            DIEU_HOA: air_info_display,
            ATS: ats_display,
            SETTING: setting_display,
            RFID: rfid_display
        }
        if start_flag is True:
            clear_display()
            start_flag = False
        clear_event()
        if screen_lv1_index != ESC:
            back_main_screen(button)
        if button in MENU_LV_1 and last_screen_lv1_index != button:
            screen_lv1_index = button
            setting_screen_index = 0
            last_screen_lv1_index = screen_lv1_index
            move_default_var()
            clear_display()
            remove_json_file()
            # get_default_value()
            reset_params_main_display()
            ats_reset_params()
            rfid_reset_params()
            reset_parameter()  # reset param in setting_screen_lcd
            setting_datetime_screen_lcd_services.get_default_value()  # reset param in datetime setting
            setting_info_screen_lcd_services.get_default_value()  # reset param in info setting
            setting_acm_screen_lcd_services.acm_setting_set_default_value()  # reset param in acm setting
        elif button != -1:
            event = button

        func = menu_function_list.get(screen_lv1_index)
        return func()
    except Exception as ex:
        LOGGER.warning('print_screen function error: %s', ex.message)
