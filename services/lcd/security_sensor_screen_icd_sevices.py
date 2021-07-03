# TRUONG
from config import *
from config.common import *
from config.common_lcd_services import *
from operate.lcd_thread import create_cmd_multi


def default_security_sensor_screen(_telemitries):
    try:
        mccSmokeState = _telemitries.get("mccSmokeState")
        mccFireState = _telemitries.get("mccFireState")
        mccFloodState = _telemitries.get("mccFloodState")

        # tao String mac dinh in ra man hinh
        screen_name = "CAM BIEN AN NINH" + SALT_DOLLAR_SIGN + str(ROW_1) + END_CMD
        smoke_tate = "Khoi: " + str(mccSmokeState) + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD
        fire_tate = "Chay: " + str(mccFireState) + SALT_DOLLAR_SIGN + str(ROW_3) + END_CMD
        flood_tate = "Ngap nuoc: " + str(mccFloodState) + SALT_DOLLAR_SIGN + str(ROW_4) + END_CMD

        cmd_lcd[UPDATE_VALUE] = screen_name + smoke_tate + fire_tate + flood_tate

    except Exception as ex:
        LOGGER.error('operate > icd_thread > default_security_sensor_screen: %s', ex.message)

def chance_security_sensor_screen(_telemitries, _moving_screen):
    try:
        cmd_lcd[UPDATE_VALUE] = create_cmd_multi("CAM BIEN AN NINH", ROW_1)
        if not _moving_screen:
            if _telemitries.get("mccSmokeState") == 1:
                cmd_lcd[UPDATE_VALUE] = "Khoi: 1" + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD
            if _telemitries.get("mccFireState") == 1:
                cmd_lcd[UPDATE_VALUE] = "Chay: 1" + SALT_DOLLAR_SIGN + str(ROW_3) + END_CMD
            if _telemitries.get("mccFloodState") == 1:
                cmd_lcd[UPDATE_VALUE] = "Ngap: 1" + SALT_DOLLAR_SIGN + str(ROW_4) + END_CMD
        else:
            if _telemitries.get("mccFloodState") == 1:
                cmd_lcd[UPDATE_VALUE] = "Ngap: 1" + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD
            if _telemitries.get("mccDoorButton") == 1:
                cmd_lcd[UPDATE_VALUE] = "Cua: 1" + SALT_DOLLAR_SIGN + str(ROW_3) + END_CMD
            if _telemitries.get("mccMoveState") == 1:
                cmd_lcd[UPDATE_VALUE] = "Chuyen dong: 1" + SALT_DOLLAR_SIGN + str(ROW_4) + END_CMD
    except Exception as ex:
        LOGGER.error('operate > icd_thread > chance_security_sensor_screen: %s', ex.message)
