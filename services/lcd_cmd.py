from config.common import UPDATE_VALUE, END_CMD, CLEAR
from config import *
from config.common_lcd_services import *


def add_cmd_lcd(dict_cmd):
    cmd = ''
    for i in dict_cmd:
        cmd += dict_cmd[i]
    cmd_lcd[UPDATE_VALUE] = cmd


def create_cmd_rule(dict_cmd, string, row):
    dict_cmd[str(row)] = str(string) + SALT_DOLLAR_SIGN + str(row) + END_CMD


def print_lcd(string, row):
    try:
        LOGGER.info('Enter print_lcd function')
        create_cmd_rule(dict_cmd, string, row)
        add_cmd_lcd(dict_cmd)
        LOGGER.info('Exit print_lcd function')
    except Exception as ex:
        LOGGER.info('Fail to connect to server with message: %s', ex.message)


def clear_display():
    cmd_lcd[CLEAR] = ''
