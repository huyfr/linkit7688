from utility import bytes_to_int
from .utils import _read_attribute, _read_telemetry
from config import BYTE_ORDER


def extract(byte_data):
    # client attributes
    atsVacP1State = bytes_to_int(byte_data[0])
    atsVacP2State = bytes_to_int(byte_data[1])
    atsVacP3State = bytes_to_int(byte_data[2])
    atsVgenP1State = bytes_to_int(byte_data[3])
    atsVgenP2State = bytes_to_int(byte_data[4])
    atsVgenP3State = bytes_to_int(byte_data[5])
    atsContactorElecState = bytes_to_int(byte_data[6])
    atsContactorGenState = bytes_to_int(byte_data[7])
    atsAcState = bytes_to_int(byte_data[8])
    atsGenState = bytes_to_int(byte_data[9])
    atsState = bytes_to_int(byte_data[10])
    atsErrorState = bytes_to_int(byte_data[11])
    atsMode = bytes_to_int(byte_data[12])
    atsConnect = bytes_to_int(byte_data[13])

    # uncomment when update STM32
    # atsVgenThresholdState = bytes_to_int(byte_data[50])
    # atsVacThresholdState = bytes_to_int(byte_data[51])

    #telemetry
    atsVacFreq = bytes_to_int(byte_data[14:16], byteorder=BYTE_ORDER)
    atsVgenFreq = bytes_to_int(byte_data[16:18], byteorder=BYTE_ORDER)
    atsVloadFreq = bytes_to_int(byte_data[18:20], byteorder=BYTE_ORDER)
    atsVacP1 = bytes_to_int(byte_data[20:22], byteorder=BYTE_ORDER)
    atsVacP2 = bytes_to_int(byte_data[22:24], byteorder=BYTE_ORDER)
    atsVacP3 = bytes_to_int(byte_data[24:26], byteorder=BYTE_ORDER)
    atsVgenP1 = bytes_to_int(byte_data[26:28], byteorder=BYTE_ORDER)
    atsVgenP2 = bytes_to_int(byte_data[28:30], byteorder=BYTE_ORDER)
    atsVgenP3 = bytes_to_int(byte_data[30:32], byteorder=BYTE_ORDER)
    atsVloadP1 = bytes_to_int(byte_data[32:34], byteorder=BYTE_ORDER)
    atsVloadP2 = bytes_to_int(byte_data[34:36], byteorder=BYTE_ORDER)
    atsVloadP3 = bytes_to_int(byte_data[36:38], byteorder=BYTE_ORDER)
    atsIloadP1 = bytes_to_int(byte_data[38:40], byteorder=BYTE_ORDER)
    atsIloadP2 = bytes_to_int(byte_data[40:42], byteorder=BYTE_ORDER)
    atsIloadP3 = bytes_to_int(byte_data[42:44], byteorder=BYTE_ORDER)
    atsPac1 = bytes_to_int(byte_data[44:46], byteorder=BYTE_ORDER)
    atsPac2 = bytes_to_int(byte_data[46:48], byteorder=BYTE_ORDER)
    atsPac3 = bytes_to_int(byte_data[48:50], byteorder=BYTE_ORDER)

    # telemetry
    _read_telemetry('atsVacFreq', atsVacFreq)
    _read_telemetry('atsVgenFreq', atsVgenFreq)
    _read_telemetry('atsVloadFreq', atsVloadFreq)
    _read_telemetry('atsVacP1', atsVacP1)
    _read_telemetry('atsVacP2', atsVacP2)
    _read_telemetry('atsVacP3', atsVacP3)
    _read_telemetry('atsVgenP1', atsVgenP1)
    _read_telemetry('atsVgenP2', atsVgenP2)
    _read_telemetry('atsVgenP3', atsVgenP3)
    _read_telemetry('atsVloadP1', atsVloadP1)
    _read_telemetry('atsVloadP2', atsVloadP2)
    _read_telemetry('atsVloadP3', atsVloadP3)
    _read_telemetry('atsIloadP1', atsIloadP1)
    _read_telemetry('atsIloadP2', atsIloadP2)
    _read_telemetry('atsIloadP3', atsIloadP3)
    _read_telemetry('atsPac1', atsPac1)
    _read_telemetry('atsPac2', atsPac2)
    _read_telemetry('atsPac3', atsPac3)


    #client attributes
    _read_attribute('atsVacP1State', atsVacP1State)
    _read_attribute('atsVacP2State', atsVacP2State)
    _read_attribute('atsVacP3State', atsVacP3State)
    _read_attribute('atsVgenP1State', atsVgenP1State)
    _read_attribute('atsVgenP2State', atsVgenP2State)
    _read_attribute('atsVgenP3State', atsVgenP3State)
    _read_attribute('atsContactorElecState', atsContactorElecState)
    _read_attribute('atsContactorGenState', atsContactorGenState)
    _read_attribute('atsAcState', atsAcState)
    _read_attribute('atsGenState', atsGenState)
    _read_attribute('atsState', atsState)
    _read_attribute('atsErrorState', atsErrorState)
    _read_attribute('atsMode', atsMode)
    _read_attribute('atsConnect', atsConnect)

    # uncomment when update STM32
    # _read_attribute('atsVgenThresholdState', atsVgenThresholdState)
    # _read_attribute('atsVacThresholdState', atsVacThresholdState)
