# TRUONG
from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *
from control import process_cmd_lcd


# man hinh mac dinh
def security_sensor_screen_1(_telemitries):
    try:
        mcc_smoke_tate = ''
        mcc_fire_state = ''
        mcc_flood_state = ''

        # thay doi cac state neu co trong telemetries, neu khong se dung mac dinh la ''
        if "mccSmokeState" in _telemitries.keys():
            mcc_smoke_tate = _telemitries.get("mccSmokeState")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_1: key 'mccSmokeState' is not in Telemetries")

        if "mccFireState" in _telemitries.keys():
            mcc_fire_state = _telemitries.get("mccFireState")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_1: key 'mccFireState' is not in Telemetries")

        if "mccFloodState" in _telemitries.keys():
            mcc_flood_state = _telemitries.get("mccFloodState")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_1: key 'mccFloodState' is not in Telemetries")

        # In ra man hinh
        process_cmd_lcd(ROW_1, UPDATE_VALUE, "CAM BIEN AN NINH")
        process_cmd_lcd(ROW_2, UPDATE_VALUE, "Khoi: " + str(mcc_smoke_tate))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, "Chay: " + str(mcc_fire_state))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, "Ngap nuoc: " + str(mcc_flood_state))

    except Exception as ex:
        LOGGER.error('operate > icd_thread > default_security_sensor_screen: %s', ex.message)


def security_sensor_screen_2(_telemitries):
    try:
        mcc_flood_state = ''
        mcc_door_button = ''
        mcc_move_state = ''

        # tao String mac dinh in ra man hinh
        if "mccFloodState" in _telemitries.keys():
            mcc_flood_state = _telemitries.get("mccFloodState")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_2: key 'mccFloodState' is not in Telemetries")

        if "mccDoorButton" in _telemitries.keys():
            mcc_door_button = _telemitries.get("mccDoorButton")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_2: key 'mccDoorButton' is not in Telemetries")

        if "mccMoveState" in _telemitries.keys():
            mcc_move_state = _telemitries.get("mccMoveState")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_2: key 'mccMoveState' is not in Telemetries")

        # In ra man hinh
        process_cmd_lcd(ROW_1, UPDATE_VALUE, "CAM BIEN AN NINH")
        process_cmd_lcd(ROW_2, UPDATE_VALUE, "Ngap: " + str(mcc_flood_state))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, "Cua: " + str(mcc_door_button))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, "Chuyen dong: " + str(mcc_move_state))
    except Exception as ex:
        LOGGER.error('operate > icd_thread > chance_security_sensor_screen: %s', ex.message)
