import time

from config import *
from config.common import UPDATE_VALUE, END_CMD, CLEAR
from config.common_lcd_services import *
from services.lcd.alarm_lcd_services import alarm_lcd_service
from services.lcd.main_screen_lcd_services import main_screen
from services.lcd.rfid_screen_lcd_sevices import rfid_screen

BAN_TIN_CANH_BAO = 'BAN TIN CANH BAO'


def add_cmd_lcd(dict_cmd):
    cmd = ''
    for i in dict_cmd:
        cmd += dict_cmd[i]
    cmd_lcd[UPDATE_VALUE] = cmd


def creat_cmd_rule(dict_cmd, string, row):
    dict_cmd[str(row)] = str(string) + SALT_DOLLAR_SIGN + str(row) + END_CMD


class Display:
    def __init__(self):
        self.last_menu = '0'

    def clear_display(self):
        # cmd_lcd[CLEAR] = ''
        self.print_lcd(' ', ROW_1)
        self.print_lcd(' ', ROW_2)
        self.print_lcd(' ', ROW_3)
        self.print_lcd(' ', ROW_4)

    def print_lcd(self, string, row):
        try:
            LOGGER.info('Enter print_lcd function')
            creat_cmd_rule(dict_cmd, string, row)
            add_cmd_lcd(dict_cmd)
            LOGGER.info('Exit print_lcd function')
        except Exception as ex:
            LOGGER.info('Fail to connect to server with message: %s', ex.message)

    def main_display(self):
        try:
            # USER CODE BEGIN
            self.clear_display()
            # self.print_lcd('1.Main display', ROW_3)
            mainScreen = main_screen()
            mainScreen.get_title_main()
            while True:
                if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_11_EVENT_UP]):
                    self.menu(button_status[0])
                mainScreen.get_user_tram()
                mainScreen.get_temp_tram()
                mainScreen.get_datetime_now()
                time.sleep(3)
                # lcd_services['key_code'] = KEYCODE_13
                # lcd_services['key_event'] = EVENT_UP
            # USER CODE END
        except Exception as ex:
            LOGGER.error('Error at call function in menu.python with message: %s', ex.message)

    def warning_display(self):
        try:
            # USER CODE BEGIN
            self.clear_display()
            # self.print_lcd('2. Warning display', ROW_1)
            warning_service = alarm_lcd_service()
            cmd_lcd[UPDATE_VALUE] = warning_service.create_cmd_multi(BAN_TIN_CANH_BAO, ROW_1)
            while True:
                if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_12_EVENT_UP]):
                    LOGGER.info('Send button value : %s', str(button_status[0]))
                    self.menu(button_status[0])
                LOGGER.info('List telemitries: %s', telemetries)
                if telemetries:
                    warning_service.check_alarm(telemetries)
                time.sleep(3)
            # USER CODE END
        except Exception as ex:
            LOGGER.error('Error at call function in menu.python with message: %s', ex.message)

    def security_sensor_info_display(self):
        # USER CODE BEGIN
        self.clear_display()
        self.print_lcd('3. Secure sensor', ROW_1)
        while True:
            if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_31_EVENT_UP]):
                LOGGER.info('Send button value : %s', str(button_status[0]))
                self.menu(button_status[0])
        # USER CODE END

    def air_info_display(self):
        # USER CODE BEGIN
        self.clear_display()
        self.print_lcd('4. Air condition', ROW_1)
        while True:
            if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_13_EVENT_UP]):
                LOGGER.info('Send button value : %s', str(button_status[0]))
                self.menu(button_status[0])
            # lcd_services['key_code'] = KEYCODE_11
            # lcd_services['key_event'] = EVENT_UP
        # USER CODE END

    def ats_display(self):
        # USER CODE BEGIN
        self.clear_display()
        self.print_lcd('5. ATS display', ROW_1)
        while True:
            if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_35_EVENT_UP]):
                LOGGER.info('Send button value : %s', str(button_status[0]))
                self.menu(button_status[0])
        # USER CODE END

    def rfid_display(self):
        # USER CODE BEGIN
        self.clear_display()
        # self.print_lcd('7. RFID display', ROW_1)
        rfidScreen = rfid_screen()
        rfidScreen.get_title_rfid()
        while True:
            if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_15_EVENT_UP]):
                LOGGER.info('Send button value : %s', str(button_status[0]))
                self.menu(button_status[0])
            rfidScreen.get_info_rfid()
            time.sleep(3)
        # USER CODE END

    def menu(self, number_menu):
        try:
            LOGGER.info('Enter menu function')
            if number_menu in MENU:
                self.last_menu = MENU[number_menu]
                return getattr(self, 'case_' + str(MENU[number_menu]))()
            else:
                return getattr(self, 'case_' + str(self.last_menu))()
        except Exception as ex:
            LOGGER.info('Fail to connect to server with message: %s', ex.message)

    def case_0(self):
        return self.main_display()

    def case_1(self):
        return self.warning_display()

    def case_2(self):
        return self.security_sensor_info_display()

    def case_3(self):
        return self.air_info_display()

    def case_4(self):
        return self.ats_display()

    def case_5(self):
        return self.setting_display()

    def case_6(self):
        return self.rfid_display()

    def setting_display(self):
        try:
            LOGGER.info('Enter setting_display function')
            mode_setting = 0
            self.clear_display()
            self.print_lcd('CAI DAT HE THONG', ROW_1)
            self.print_lcd('-> TT he thong  ', ROW_2)
            self.print_lcd('   Thoi gian    ', ROW_3)
            self.print_lcd('   Thong so mang', ROW_4)
            while True:
                last_mode = mode_setting
                if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_33_EVENT_UP]):
                    LOGGER.info('Send button value : %s', str(button_status[0]))
                    self.menu(button_status[0])
                if button_status[0] == BUTTON_14_EVENT_UP:
                    mode_setting += 1
                elif button_status[0] == BUTTON_34_EVENT_UP:
                    mode_setting -= 1
                elif button_status[0] == BUTTON_23_EVENT_UP:
                    mode_setting = 0
                elif button_status[0] == BUTTON_25_EVENT_UP:
                    mode_setting = 3
                if mode_setting > 5:
                    mode_setting = 5
                elif mode_setting < 0:
                    mode_setting = 0

                if mode_setting != last_mode:
                    LOGGER.info('mode setting : %s', str(mode_setting))
                    LOGGER.info('Send button value : %s', str(button_status[0]))
                    self.setting_menu(mode_setting)

                if button_status[0] == BUTTON_24_EVENT_UP:
                    LOGGER.info('Send button value : %s', str(button_status[0]))
                    pass  # vao man hinh setting thong so da chon

        except Exception as ex:
            LOGGER.info('Fail to connect to server with message: %s', ex.message)

    def setting_menu(self, setting_mode):
        try:
            LOGGER.info('Enter setting_menu function')
            return getattr(self, 'setting_menu_' + str(setting_mode))()
        except Exception as ex:
            LOGGER.info('Fail to connect to server with message: %s', ex.message)

    def setting_menu_0(self):
        # USER CODE BEGIN
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('-> TT he thong  ', ROW_2)
        self.print_lcd('   Thoi gian    ', ROW_3)
        self.print_lcd('   Thong so mang', ROW_4)

        # USER CODE END

    def setting_menu_1(self):
        # USER CODE BEGIN
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('   TT he thong  ', ROW_2)
        self.print_lcd('-> Thoi gian    ', ROW_3)
        self.print_lcd('   Thong so mang', ROW_4)

        # USER CODE END

    def setting_menu_2(self):
        # USER CODE BEGIN
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('   TT he thong  ', ROW_2)
        self.print_lcd('   Thoi gian    ', ROW_3)
        self.print_lcd('-> Thong so mang', ROW_4)

        # USER CODE END

    def setting_menu_3(self):
        # USER CODE BEGIN
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('-> Canh bao     ', ROW_2)
        self.print_lcd('   ATS          ', ROW_3)
        self.print_lcd('   Phu kien     ', ROW_4)

        # USER CODE END

    def setting_menu_4(self):
        # USER CODE BEGIN
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('   Canh bao     ', ROW_2)
        self.print_lcd('-> ATS          ', ROW_3)
        self.print_lcd('   Phu kien     ', ROW_4)

        # USER CODE END

    def setting_menu_5(self):
        # USER CODE BEGIN
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('   Canh bao     ', ROW_2)
        self.print_lcd('   ATS          ', ROW_3)
        self.print_lcd('-> Phu kien     ', ROW_4)

        # USER CODE END

