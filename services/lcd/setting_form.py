from config import *
from config.common import END_CMD, UPDATE_VALUE
from config.common_lcd_services import *


# Tra ve 1 form mau chung:
# _name_of_screen: string: hien thi ten man hinh tren dong dau tien
# _option1, 2, 3: string: cac lua chon cua man hinh, toi da 3 lua chon,
# neu ko co lua chon, truyen vao string rong ""
# _selected_option: number: la lua chon dang duoc chon, co 3 gia tri 1, 2, 3
from control import process_cmd_lcd


def setting_screen_form(_name_of_screen, _selected_option, _option1, _option2, _option3):
    line1 = _option1
    line2 = _option2
    line3 = _option3

    if _selected_option == 1:
        line1 = ">" + _option1
    elif _selected_option == 2:
        line2 = ">" + _option2
    elif _selected_option == 3:
        line3 = ">" + _option3
    else:
        LOGGER.error("services > icd > setting_form.py: _selected_option must be 1, 2 or 3")
    process_cmd_lcd(ROW_1, UPDATE_VALUE, _name_of_screen)
    process_cmd_lcd(ROW_2, UPDATE_VALUE, line1)
    process_cmd_lcd(ROW_3, UPDATE_VALUE, line2)
    process_cmd_lcd(ROW_4, UPDATE_VALUE, line3)


# man hinh xac nhan luu, truyen vao _selected_option: number, gia tri 1: Co, 2: Khong
def accept_screen(_selected_option):
    if _selected_option == 1 or _selected_option == 2:
        return setting_screen_form("XAC NHAN LUU", _selected_option, "Co", "Khong", "")
    else:
        LOGGER.error("services > icd > accept_screen.py: _selected_option must be 1 or 2")
