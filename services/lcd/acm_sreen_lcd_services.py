from config import LOGGER, telemetries
from config.common import UPDATE_VALUE
from config.common_lcd_services import *


def show_temp_condition(_telemetries):
    from control import process_cmd_lcd

    try:
        process_cmd_lcd(ROW_1, UPDATE_VALUE, 'BAN TIN DIEU HOA')
        LOGGER.info('Check Telemetries: %s', _telemetries)

        if 'acmAirc1RunState' and 'acmAirc2RunState' in _telemetries:
            temp1 = _telemetries['acmAirc1RunState']
            temp2 = _telemetries['acmAirc2RunState']

            if temp1 == 0 and temp2 == 0:
                process_cmd_lcd(ROW_2, UPDATE_VALUE, 'DH1:Tat DH2:Tat')
            elif temp1 == 1 and temp2 == 1:
                process_cmd_lcd(ROW_2, UPDATE_VALUE, 'DH1:Bat DH2: Bat')
            elif temp1 == 1 and temp2 == 0:
                process_cmd_lcd(ROW_2, UPDATE_VALUE, 'DH1:Bat DH2: Tat')
            elif temp1 == 0 and temp2 == 1:
                process_cmd_lcd(ROW_2, UPDATE_VALUE, 'DH1:Tat DH2: Bat')
        else:
            LOGGER.error("services > lcd > air_screen_lcd_services ")

        if 'acmFanRunState' in _telemetries:
            mode_fan = _telemetries['acmFanRunState']
            if mode_fan == 1:
                process_cmd_lcd(ROW_3, UPDATE_VALUE, 'Quat: Bat')
            elif mode_fan == 0:
                process_cmd_lcd(ROW_3, UPDATE_VALUE, 'Quat: Tat')

        if 'acmAutoMode' in _telemetries:
            mode_auto = _telemetries['acmAutoMode']
            if mode_auto == 1:
                process_cmd_lcd(ROW_4, UPDATE_VALUE, 'Che do: Auto')
            elif mode_auto == 0:
                process_cmd_lcd(ROW_4, UPDATE_VALUE, 'Che do: Manual')

    except Exception as ex:
        LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)
