from config import *
from control.utils import read_to_json, write_to_json
data_setting_path = '../../lcd_setting_data_file.json'

# {
#     "auto": 0,
#     "grid_electric": 0,
#     "generator": 0
#   }

def updateSettingATS(dict):
    data = read_to_json(data_setting_path)
    data['setting_ats'] = dict
    write_to_json(data, data_setting_path)




