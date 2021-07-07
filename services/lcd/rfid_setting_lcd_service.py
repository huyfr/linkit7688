from config import *
from control.utils import read_to_json, write_to_json
data_setting_path = '../../lcd_setting_data_file.json'

# "setting_rfid_allow": 0
# 0 - not allow
# 1 - allow
def updateSettingRFID(setting_rfid_allow):
    data = read_to_json(data_setting_path)
    data['setting_rfid_allow'] = setting_rfid_allow
    write_to_json(data, data_setting_path)




