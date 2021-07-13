from config import *
from config.common import *
from config.common_lcd_services import *

info = ['_'] * 16

level_at_index = [0] * 16

char = [chr(i) for i in range(ord('A'), ord('A') + 26)]
char.append(" ")

confirm_status = False

confirm_idx = 0

cursor_idx = 0

ok_time = 0


def call_screen_confirm(p_idx):
    from control import process_cmd_lcd
    try:
        switcher = [
            {
                "row_2": '> Co',
                "row_3": 'Khong'
            },
            {
                "row_2": 'Co',
                "row_3": '> Khong'
            }
        ]
        # Update text
        process_cmd_lcd(ROW_1, UPDATE_VALUE, 'XAC NHAN')
        process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[p_idx]['row_2'])
        process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[p_idx]['row_3'])
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


def info_setting_process(button):
    from control import process_cmd_lcd
    global ok_time
    global confirm_idx
    global cursor_idx
    global confirm_status
    global char
    try:
        if ok_time > 1:
            confirm_status = True
        if confirm_status:
            if button == OK:
                if confirm_idx == 0:
                    a_file = open("./lcd_setting_data_file.json", "r")
                    json_object = json.load(a_file)
                    a_file.close()
                    json_object["setting_info_title"] = ''.join(info)
                    a_file = open("./lcd_setting_data_file.json", "w")
                    json.dump(json_object, a_file)
                    a_file.close()
                    confirm_status = False
                    # ham thoat
                    process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THONG TIN')
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(info))
                    ok_time = 1
                    confirm_idx = -1
                else:
                    process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THONG TIN')
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(info))
                    ok_time = 1
                    confirm_idx = -1
                    confirm_status = False
            elif button == UP or button == DOWN:
                if confirm_idx == 0 or confirm_idx == -1:
                    confirm_idx = 1
                else:
                    confirm_idx = 0
        else:
            if button == OK:
                if ok_time == 1:
                    call_screen_confirm(0)

                ok_time += 1
                # process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THONG TIN')
                # process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(info))

                # confirm_status = True

            else:
                if button == UP:
                    level_at_index[cursor_idx] += 1

                    if level_at_index[cursor_idx] > len(char) - 1:
                        level_at_index[cursor_idx] = 0

                    info[cursor_idx] = char[level_at_index[cursor_idx]]
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(info))
                elif button == DOWN:
                    level_at_index[cursor_idx] -= 1
                    if level_at_index[cursor_idx] < 0:
                        level_at_index[cursor_idx] = len(char) - 1
                    info[cursor_idx] = char[level_at_index[cursor_idx]]
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(info))
                elif button == RIGHT:
                    cursor_idx += 1
    except Exception as ex:
        LOGGER.error('Error at call function in info_setting_process with message: %s', ex.message)