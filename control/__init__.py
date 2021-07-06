from config import LOGGER
from . import utils


def process_set_auto(command):
    return utils._process_set_auto(command.get('device', None), command.get('command', None))


def check_command(command):
    return utils._check_command(command.get('device', None), command.get('command', None))


def check_command_send_rpc(command):
    try:
        return utils._check_command_send_rpc(command.get('device', None), command.get('command', None))
    except Exception as ex:
        print(ex.message)
        LOGGER.error('Error at check_command_send_rpc function with message: %s', ex.message)


def process_command(command):
    return utils._process_command(command['device'], command['command'])


def process_cmd_led(cmd_led):
    return utils._process_cmd_led(cmd_led['length_led'], cmd_led['arr_value'])


def process_cmd_lcd(cmd_lcd):
    return utils._process_cmd_lcd(cmd_lcd['key_lcd'], cmd_lcd['content'])

# def process_cmd_lcd(row, key_lcd, content):
#     return utils._process_cmd_lcd(row, key_lcd, content)


def process_cmd_sa(cmd_sa):
    return utils._process_cmd_sa(cmd_sa['module_id'], cmd_sa['value'])

