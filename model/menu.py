import sys
import time

from config import *
from config.common_lcd_services import *
from services.lcd.rfid_screen_lcd_sevices import rfid_screen
from services import lcd_cmd
from services.lcd.security_sensor_screen_icd_sevices import *
class Display:
    def __init__(self):
        self.last_menu = '0'

    def main_display(self):
        try:
            # USER CODE BEGIN
            lcd_cmd.clear_display()
            # self.print_lcd('1.Main display', ROW_3)
            # button_status[0] = str(MENU[BUTTON_12_EVENT_UP])
            while True:
                if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_11_EVENT_UP]):
                    # Recheck = {"title": '', "time": '61', "acmTempOutdoor": 0, "acmHumidIndoor": 0, "acmTempIndoor": 0, "isWarning": ""}
                    # write_to_json(Recheck, './main_screen.json')
                    self.menu(button_status[0])
                # mainScreen = main_screen()
                # mainScreen.get_datetime_title_now()
                # mainScreen.get_temp_tram()
                # mainScreen.get_user_tram()
                # time.sleep(3)
                # lcd_services['key_code'] = KEYCODE_13
                # lcd_services['key_event'] = EVENT_UP
            # USER CODE END
        except Exception as ex:
            LOGGER.error('Error at call function in menu.python with message: %s', ex.message)

    def warning_display(self):
        try:
            # USER CODE BEGIN
            lcd_cmd.clear_display()
            # warning_service = alarm_lcd_service()
            while True:
                if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_12_EVENT_UP]):
                    LOGGER.info('Send button value : %s', str(button_status[0]))
                    self.menu(button_status[0])
                # else:
                    # warning_service.check_alarm(tel_lcd=telemetries)
                time.sleep(3)
            # USER CODE END
        except Exception as ex:
            LOGGER.error('Error at call function in menu.python with message: %s', ex.message)

    def security_sensor_info_display(self):
        pass
        # USER CODE BEGIN
        # lcd_cmd.clear_display()
        # # lcd_cmd.print_lcd('3. Secure sensor', ROW_1)
        #         if telemetries:
        #     default_security_sensor_screen(telemetries)
        #     while True:
        #         if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_31_EVENT_UP]):
        #             LOGGER.info('Send button value : %s', str(button_status[0]))
        #             self.menu(button_status[0]) # ??????
        #         if True: #(check button sang phai):
        #             chance_security_sensor_screen(telemetries, True)
        #         if True: #(check button sang trai):
        #             chance_security_sensor_screen(telemetries, False)
        # else:
        #     LOGGER.error("model > menu > security_sensor_info_display: can not get telemetries ")
            # USER CODE END

    def air_info_display(self):
        # USER CODE BEGIN
        lcd_cmd.clear_display()
        lcd_cmd.print_lcd('4. Air condition', ROW_1)
        while True:
            if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_13_EVENT_UP]):
                LOGGER.info('Send button value : %s', str(button_status[0]))
                self.menu(button_status[0])
            # lcd_services['key_code'] = KEYCODE_11
            # lcd_services['key_event'] = EVENT_UP
        # USER CODE END

    # def ats_display(self):
    #     # USER CODE BEGIN
    #     goto_display = 1
    #     lcd_cmd.clear_display()
    #     # ats_service.header()
    #     while True:
    #         if button_status[0] in MENU and button_status[0] != BUTTON_35_EVENT_UP:
    #             LOGGER.info('Send button value : %s', str(button_status[0]))
    #             self.menu(button_status[0])
    #         if button_status[0] == BUTTON_25_EVENT_UP:
    #             goto_display = 2
    #             lcd_cmd.clear_display()
    #         elif button_status[0] == BUTTON_23_EVENT_UP:
    #             goto_display = 1
    #             lcd_cmd.clear_display()
    #
    #         # if goto_display == 1:
    #         #     # ats_service.display1()
    #         # elif goto_display == 2:
    #         #     ats_service.display2()
    #         time.sleep(3)
    #     # USER CODE END

    def rfid_display(self):
        try:
            lcd_cmd.clear_display()
            # self.print_lcd('7. RFID display', ROW_1)
            rfidScreen = rfid_screen()
            rfidScreen.get_title_rfid()
            while True:
                if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_15_EVENT_UP]):
                    LOGGER.info('Send button value : %s', str(button_status[0]))
                    self.menu(button_status[0])
                rfidScreen.get_info_rfid()
                time.sleep(3)
        except Exception as ex:
            LOGGER.error('Error at rfid_display function with message: %s', ex.message)
            sys.exit(1)

    def menu(self, number_menu):
        try:
            LOGGER.info('Enter menu function')
            if number_menu in MENU:
                self.last_menu = MENU[number_menu]
                return getattr(self, 'case_' + str(MENU[number_menu]))()
            else:
                return getattr(self, 'case_' + str(self.last_menu))()
        except Exception as ex:
            LOGGER.info('menu function error: %s', ex.message)

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
            lcd_cmd.clear_display()
            lcd_cmd.print_lcd('CAI DAT HE THONG', ROW_1)
            lcd_cmd.print_lcd('-> TT he thong  ', ROW_2)
            lcd_cmd.print_lcd('   Thoi gian    ', ROW_3)
            lcd_cmd.print_lcd('   Thong so mang', ROW_4)
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
            LOGGER.info('setting_display function error: %s', ex.message)

    def setting_menu(self, setting_mode):
        try:
            LOGGER.info('Enter setting_menu function')
            return getattr(self, 'setting_menu_' + str(setting_mode))()
        except Exception as ex:
            LOGGER.info('switch setting menu false: %s', ex.message)

    def setting_menu_0(self):
        # USER CODE BEGIN
        lcd_cmd.print_lcd('CAI DAT HE THONG', ROW_1)
        lcd_cmd.print_lcd('-> TT he thong  ', ROW_2)
        lcd_cmd.print_lcd('   Thoi gian    ', ROW_3)
        lcd_cmd.print_lcd('   Thong so mang', ROW_4)

        # USER CODE END

    def setting_menu_1(self):
        # USER CODE BEGIN
        lcd_cmd.print_lcd('CAI DAT HE THONG', ROW_1)
        lcd_cmd.print_lcd('   TT he thong  ', ROW_2)
        lcd_cmd.print_lcd('-> Thoi gian    ', ROW_3)
        lcd_cmd.print_lcd('   Thong so mang', ROW_4)

        # USER CODE END

    def setting_menu_2(self):
        # USER CODE BEGIN
        lcd_cmd.print_lcd('CAI DAT HE THONG', ROW_1)
        lcd_cmd.print_lcd('   TT he thong  ', ROW_2)
        lcd_cmd.print_lcd('   Thoi gian    ', ROW_3)
        lcd_cmd.print_lcd('-> Thong so mang', ROW_4)

        # USER CODE END

    def setting_menu_3(self):
        # USER CODE BEGIN
        lcd_cmd.print_lcd('CAI DAT HE THONG', ROW_1)
        lcd_cmd.print_lcd('-> Canh bao     ', ROW_2)
        lcd_cmd.print_lcd('   ATS          ', ROW_3)
        lcd_cmd.print_lcd('   Phu kien     ', ROW_4)

        # USER CODE END

    def setting_menu_4(self):
        # USER CODE BEGIN
        lcd_cmd.print_lcd('CAI DAT HE THONG', ROW_1)
        lcd_cmd.print_lcd('   Canh bao     ', ROW_2)
        lcd_cmd.print_lcd('-> ATS          ', ROW_3)
        lcd_cmd.print_lcd('   Phu kien     ', ROW_4)

        # USER CODE END

    def setting_menu_5(self):
        # USER CODE BEGIN
        lcd_cmd.print_lcd('CAI DAT HE THONG', ROW_1)
        lcd_cmd.print_lcd('   Canh bao     ', ROW_2)
        lcd_cmd.print_lcd('   ATS          ', ROW_3)
        lcd_cmd.print_lcd('-> Phu kien     ', ROW_4)

        # USER CODE END
