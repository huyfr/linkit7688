from config import BYTE_ORDER
from utility import bytes_to_int
from .utils import _read_attribute, _read_telemetry


def extract(byte_data):
    #telemetry
    mccSmokeState = bytes_to_int(byte_data[0])
    mccFireState = bytes_to_int(byte_data[1])
    mccMoveState = bytes_to_int(byte_data[2])
    mccDoorState = bytes_to_int(byte_data[3])
    mccDin6 = bytes_to_int(byte_data[4])
    mccDin7 = bytes_to_int(byte_data[5])
    mccFloodState = bytes_to_int(byte_data[6])
    mccDoorButton = bytes_to_int(byte_data[7])
    mccBellState = bytes_to_int(byte_data[8])
    mccDeviceTemp = bytes_to_int(byte_data[9:11], byteorder=BYTE_ORDER)
    mccRackTemp = bytes_to_int(byte_data[11:13], byteorder=BYTE_ORDER)
    mccDcBat1Temp = bytes_to_int(byte_data[13:15], byteorder=BYTE_ORDER)
    mccDcBat2Temp = bytes_to_int(byte_data[15:17], byteorder=BYTE_ORDER)
    mccDcBat3Temp = bytes_to_int(byte_data[17:19], byteorder=BYTE_ORDER)
    mccDcAccuState = bytes_to_int(byte_data[19:21], byteorder=BYTE_ORDER)
    mccDcV1 = bytes_to_int(byte_data[21:23], byteorder=BYTE_ORDER)
    mccDcI1 = bytes_to_int(byte_data[23:25], byteorder=BYTE_ORDER)
    mccDcP1 = bytes_to_int(byte_data[25:27], byteorder=BYTE_ORDER)
    mccDcV2 = bytes_to_int(byte_data[27:29], byteorder=BYTE_ORDER)
    mccDcI2 = bytes_to_int(byte_data[29:31], byteorder=BYTE_ORDER)
    mccDcP2 = bytes_to_int(byte_data[31:33], byteorder=BYTE_ORDER)
    mccDcV3 = bytes_to_int(byte_data[33:35], byteorder=BYTE_ORDER)
    mccDcI3 = bytes_to_int(byte_data[35:37], byteorder=BYTE_ORDER)
    mccDcP3 = bytes_to_int(byte_data[37:39], byteorder=BYTE_ORDER)
    mccDcV4 = bytes_to_int(byte_data[39:41], byteorder=BYTE_ORDER)
    mccDcI4 = bytes_to_int(byte_data[41:43], byteorder=BYTE_ORDER)
    mccDcP4 = bytes_to_int(byte_data[43:45], byteorder=BYTE_ORDER)
    mccDcV5 = bytes_to_int(byte_data[45:47], byteorder=BYTE_ORDER)
    mccDcI5 = bytes_to_int(byte_data[47:49], byteorder=BYTE_ORDER)
    mccDcP5 = bytes_to_int(byte_data[49:51], byteorder=BYTE_ORDER)

    # client attributes
    mccSystemClock = bytes_to_int(byte_data[51:55], byteorder=BYTE_ORDER)
    mccRfidConnectState = bytes_to_int(byte_data[55])
    mccDcCabinetSate = bytes_to_int(byte_data[56])

    # uncomment when update code STM32
    # mccDcCabinetSate = bytes_to_int(byte_data[57])

    # telemetry
    _read_telemetry('mccSmokeState', mccSmokeState)
    _read_telemetry('mccFireState', mccFireState)
    _read_telemetry('mccMoveState', mccMoveState)
    _read_telemetry('mccDoorState', mccDoorState)
    _read_telemetry('mccBellState', mccBellState)
    _read_telemetry('mccFloodState', mccFloodState)
    _read_telemetry('mccDoorButton', mccDoorButton)
    _read_telemetry('mccDin6', mccDin6)
    _read_telemetry('mccDin7', mccDin7)
    _read_telemetry('mccDeviceTemp', mccDeviceTemp)
    _read_telemetry('mccRackTemp', mccRackTemp)
    _read_telemetry('mccDcBat1Temp', mccDcBat1Temp)
    _read_telemetry('mccDcBat2Temp', mccDcBat2Temp)
    _read_telemetry('mccDcBat3Temp', mccDcBat3Temp)
    _read_telemetry('mccDoorButton', mccDoorButton)
    _read_telemetry('mccDcAccuState', mccDcAccuState)
    _read_telemetry('mccDcV1', mccDcV1)
    _read_telemetry('mccDcI1', mccDcI1)
    _read_telemetry('mccDcP1', mccDcP1)
    _read_telemetry('mccDcV2', mccDcV2)
    _read_telemetry('mccDcI2', mccDcI2)
    _read_telemetry('mccDcP2', mccDcP2)
    _read_telemetry('mccDcV3', mccDcV3)
    _read_telemetry('mccDcI3', mccDcI3)
    _read_telemetry('mccDcP3', mccDcP3)
    _read_telemetry('mccDcV4', mccDcV4)
    _read_telemetry('mccDcI4', mccDcI4)
    _read_telemetry('mccDcP4', mccDcP4)
    _read_telemetry('mccDcV5', mccDcV5)
    _read_telemetry('mccDcI5', mccDcI5)
    _read_telemetry('mccDcP5', mccDcP5)

    # uncomment when update code STM32
    # _read_telemetry('mccDcCabinetSate', mccDcCabinetSate)

    # client attributes
    _read_attribute('mccSystemClock', mccSystemClock)
    _read_attribute('mccRfidConnectState', mccRfidConnectState)
    _read_attribute('mccDcCabinetSate', mccDcCabinetSate)
