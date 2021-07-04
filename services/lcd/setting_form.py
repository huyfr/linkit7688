from config import *
from config.common import END_CMD
from config.common_lcd_services import *


# Tra ve 1 form mau chung:
# _name_of_screen: string: hien thi ten man hinh tren dong dau tien
# _option1, 2, 3: string: cac lua chon cua man hinh, toi da 3 lua chon,
# neu ko co lua chon 3, truyen vao string rong ""
# _selected_option: number: la lua chon dang duoc chon, co 3 gia tri 1, 2, 3
def setting_screen_form(_name_of_screen, _selected_option, _option1, _option2, _option3):
    name_of_screen = _name_of_screen + SALT_DOLLAR_SIGN + str(ROW_1) + END_CMD
    line1 = _option1 + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD
    line2 = _option2 + SALT_DOLLAR_SIGN + str(ROW_3) + END_CMD
    line3 = _option3 + SALT_DOLLAR_SIGN + str(ROW_4) + END_CMD

    if _selected_option == 1:
        return name_of_screen + ">" + line1 + line2 + line3
    if _selected_option == 2:
        return name_of_screen + line1 + ">" + line2 + line3
    if _selected_option == 3:
        return name_of_screen + line1 + line2 + ">" + line3
    else:
        LOGGER.error("services > icd > setting_form.py: _selected_option must be 1, 2 or 3")
