# TRUONG
from config import *


# cmd_lcd = {1: [5, 'a'], 2: [5, 'b'], 3: [5, 'c'], 4: [5, 'd']}
# man hinh mac dinh
def security_sensor_screen_1(_telemitries):
    try:
        mccSmokeState = ''
        mccFireState = ''
        mccFloodState = ''

        if "mccSmokeState" in _telemitries.keys():
            mccSmokeState = _telemitries.get("mccSmokeState")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_1: key 'mccSmokeState' is not in Telemetries")

        if "mccFireState" in _telemitries.keys():
            mccFireState = _telemitries.get("mccFireState")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_1: key 'mccFireState' is not in Telemetries")

        if "mccFloodState" in _telemitries.keys():
            mccFloodState = _telemitries.get("mccFloodState")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_1: key 'mccFloodState' is not in Telemetries")

            # tao String mac dinh in ra man hinh
        screen_name = "CAM BIEN AN NINH"
        smoke_state = "Khoi: " + str(mccSmokeState)
        fire_state = "Chay: " + str(mccFireState)
        flood_state = "Ngap nuoc: " + str(mccFloodState)

        return {
            1: [5, screen_name],
            2: [5, smoke_state],
            3: [5, fire_state],
            4: [5, flood_state]
        }

    except Exception as ex:
        LOGGER.error('operate > icd_thread > default_security_sensor_screen: %s', ex.message)


def security_sensor_screen_2(_telemitries):
    try:
        mccFloodState = ''
        mccDoorButton = ''
        mccMoveState = ''

        # tao String mac dinh in ra man hinh
        if "mccFloodState" in _telemitries.keys():
            mccFloodState = _telemitries.get("mccFloodState")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_2: key 'mccFloodState' is not in Telemetries")

        if "mccDoorButton" in _telemitries.keys():
            mccDoorButton = _telemitries.get("mccDoorButton")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_2: key 'mccDoorButton' is not in Telemetries")

        if "mccMoveState" in _telemitries.keys():
            mccMoveState = _telemitries.get("mccMoveState")
        else:
            LOGGER.error(
                "operate > icd_thread > security_sensor_screen_2: key 'mccMoveState' is not in Telemetries")

        screen_name = "CAM BIEN AN NINH"
        flood_state = "Ngap nuoc: " + str(mccFloodState)
        door_state = "Cua: " + str(mccDoorButton)
        moving_state = "Chuyen dong: " + str(mccMoveState)

        return {
            1: [5, screen_name],
            2: [5, flood_state],
            3: [5, door_state],
            4: [5, moving_state]
        }
    except Exception as ex:
        LOGGER.error('operate > icd_thread > chance_security_sensor_screen: %s', ex.message)
