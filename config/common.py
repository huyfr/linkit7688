# device_name
from config.common_command import *

# response rfid
RESPONSE_RFID = 5

# ID DEVICE
ID_MCC = 97
ID_ACM = 99
ID_ATS = 98

# FORMAT RPC
CHAR_B = 'B'
CHAR_S = 's'
CHAR_SPACE = ' '
FORMAT_RPC = 'BBBBBB'
FORMAT_RFID = 'BBBBB'
FORMAT_LCD = 'BBBBB'
FORMAT_LED = 'BBBBB'

# BYTES SHARED ATTRIBUTES
BYTES_SA_MCC = 8
BYTES_SA_ACM = 18
BYTES_SA_ATS = 26

# SHARED ATTRIBUTES
TYPE = 'type'
ID_SHARED_ATTRIBUTES = 'idSharedAttributes'
VALUE = 'value'
MCC = 'mcc'
ACM = 'acm'
ATS = 'ats'
KEY_MCC = 'sharedMcc'
KEY_ATS = 'sharedAts'
KEY_ACM = 'sharedAcm'

# rpc
AUTO = 'setAuto'
CONTROL = 'setControl'
GET_STATE = 'getState'
GET_VALUE = 'getValue'

# lcd service
UPDATE_VALUE = 5
CLEAR = 6
END_CMD = '$@'

# list command
list_command = [COMMAND_MCC_OPEN_DOOR, COMMAND_MCC_CLOSE_DOOR, COMMAND_MCC_ON_BELL, COMMAND_MCC_OFF_BELL,
                COMMAND_MCC_ON_LAMP, COMMAND_MCC_OFF_LAMP, COMMAND_MCC_OFF_DOUT_REVERSED_1,
                COMMAND_MCC_ON_DOUT_REVERSED_1,
                COMMAND_MCC_OFF_DOUT_REVERSED_2, COMMAND_MCC_ON_DOUT_REVERSED_2, COMMAND_MCC_OFF_DOUT_REVERSED_3,
                COMMAND_MCC_ON_DOUT_REVERSED_3,
                COMMAND_MCC_OFF_DOUT_REVERSED_4, COMMAND_MCC_ON_DOUT_REVERSED_4, COMMAND_MCC_OFF_DOUT_REVERSED_5,
                COMMAND_MCC_ON_DOUT_REVERSED_5,
                COMMAND_MCC_OFF_DOUT_REVERSED_6, COMMAND_MCC_ON_DOUT_REVERSED_6, COMMAND_MCC_OFF_DOUT_REVERSED_7,
                COMMAND_MCC_ON_DOUT_REVERSED_7,
                COMMAND_MCC_OFF_DOUT_REVERSED_8, COMMAND_MCC_ON_DOUT_REVERSED_8, COMMAND_MCC_OFF_DOUT_REVERSED_9,
                COMMAND_MCC_ON_DOUT_REVERSED_9,
                COMMAND_MCC_OFF_DOUT_REVERSED_10, COMMAND_MCC_ON_DOUT_REVERSED_10, COMMAND_MCC_OFF_DOUT_REVERSED_11,
                COMMAND_MCC_ON_DOUT_REVERSED_11,
                COMMAND_MCC_OFF_DOUT_REVERSED_12, COMMAND_MCC_ON_DOUT_REVERSED_12, COMMAND_MCC_OFF_DOUT_REVERSED_13,
                COMMAND_MCC_ON_DOUT_REVERSED_13,
                COMMAND_ACM_AUTO_OFF, COMMAND_ACM_AUTO_ON, COMMAND_ACM_AIRC_1_OFF, COMMAND_ACM_AIRC_1_ON,
                COMMAND_ACM_AIRC_2_ON, COMMAND_ACM_AIRC_2_OFF, COMMAND_ACM_FAN_OFF,
                COMMAND_ACM_FAN_ON, COMMAND_ACM_SELF_PROPELLED_OFF, COMMAND_ACM_SELF_PROPELLED_ON,
                COMMAND_ATS_MAIN_ON, COMMAND_ATS_GEN_ON, COMMAND_ATS_AUTO_ON, COMMAND_ATS_OFF]
