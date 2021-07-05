# TRUONG
from config import *
from config.common import *

# cmd_lcd = {1: [5, 'a'], 2: [5, 'b'], 3: [5, 'c'], 4: [5, 'd']}

# man hinh mac dinh
def security_sensor_screen_1(_telemitries):
    try:
        mccSmokeState = _telemitries.get("mccSmokeState")
        mccFireState = _telemitries.get("mccFireState")
        mccFloodState = _telemitries.get("mccFloodState")

        # tao String mac dinh in ra man hinh
        screen_name = "CAM BIEN AN NINH"
        smoke_state = "Khoi: " + str(mccSmokeState)
        fire_state = "Chay: " + str(mccFireState)
        flood_state = "Ngap nuoc: " + str(mccFloodState)

        cmd_lcd[UPDATE_VALUE] = {
            1: [5, screen_name],
            2: [5, smoke_state],
            3: [5, fire_state],
            4: [5, flood_state]
        }
    except Exception as ex:
        LOGGER.error('operate > icd_thread > default_security_sensor_screen: %s', ex.message)


def security_sensor_screen_2(_telemitries):
    try:
        mccFloodState = _telemitries.get("mccFloodState")
        mccDoorButton = _telemitries.get("mccDoorButton")
        mccMoveState = _telemitries.get("mccMoveState")

        # tao String mac dinh in ra man hinh
        screen_name = "CAM BIEN AN NINH"
        flood_state = "Ngap nuoc: " + str(mccFloodState)
        door_state = "Khoi: " + str(mccDoorButton)
        moving_state = "Chay: " + str(mccMoveState)

        cmd_lcd[UPDATE_VALUE] = {
            1: [5, screen_name],
            2: [5, flood_state],
            3: [5, door_state],
            4: [5, moving_state]
        }
    except Exception as ex:
        LOGGER.error('operate > icd_thread > chance_security_sensor_screen: %s', ex.message)
