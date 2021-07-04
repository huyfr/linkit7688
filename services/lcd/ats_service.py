from config import *
from config.common_lcd_services import *
from operate.update_attributes_thread import replica_client_attributes
from services import lcd_cmd


is_connect = 0
ats_generator_stt = 0
ats_power_network_stt = 0
ats_vac = [0, 0, 0]
ats_vgen = [0, 0, 0]
ats_vload = [0, 0, 0]
ats_iload = [0, 0, 0]
# self.is_connect_previous = 0
# self.electricity_supply_previous = 0
#
# self.ats_vac_previous = [0, 0, 0]
# self.ats_vgen_previous = [0, 0, 0]
# self.ats_vload_previous = [0, 0, 0]
# self.ats_iload_previous = [0, 0, 0]

def header():
    lcd_cmd.print_lcd('THONG TIN ATS', ROW_1)


def disconnect_display():
    global is_connect

    if is_connect == 0:
        lcd_cmd.print_lcd('Mat ket noi', ROW_2)


def display1():
    global ats_generator_stt
    global ats_power_network_stt

    try:
        if get_state():
            header()
            if is_connect:
                lcd_cmd.print_lcd('Ket noi', ROW_2)
                if ats_power_network_stt:
                    lcd_cmd.print_lcd('Nguon: May phat', ROW_3)
                    LOGGER.info('ATS is connecting, power supply: Power generator')
                elif ats_generator_stt:
                    lcd_cmd.print_lcd('Nguon: Dien luoi', ROW_3)
                    LOGGER.info('ATS is connecting, power supply: Electric network')
            else:
                header()
                disconnect_display()
                LOGGER.info('ATS disconnected')
    except Exception as ex:
        LOGGER.info('display1 function error: %s', ex.message)


def display2():
    global is_connect
    global ats_vgen
    global ats_vac
    global ats_vload
    global ats_iload

    try:
        if get_values_ats() and get_state():
            if is_connect:
                if ats_power_network_stt:
                    string_row2 = '{p1}V {p2}V {p3}V'.format(p1=ats_vac[0], p2=ats_vac[1],
                                                             p3=ats_vac[2])
                else:
                    string_row2 = '{p1}V {p2}V {p3}V'.format(p1=ats_vgen[0], p2=ats_vgen[1],
                                                             p3=ats_vgen[2])
                lcd_cmd.print_lcd(string_row2, ROW_2)
            else:
                header()
                disconnect_display()
            lcd_cmd.print_lcd('Ket noi', ROW_2)
            string_row3 = '{p1}V {p2}V {p3}V'.format(p1=ats_vload[0], p2=ats_vload[1],
                                                     p3=ats_vload[2])
            string_row4 = '{p1}A {p2}A {p3}A'.format(p1=ats_iload[0], p2=ats_iload[1],
                                                     p3=ats_iload[2])
            lcd_cmd.print_lcd(string_row3, ROW_3)
            lcd_cmd.print_lcd(string_row4, ROW_4)
    except Exception as ex:
        LOGGER.info('display2 function error: %s', ex.message)


def get_state():
    global is_connect
    global ats_generator_stt
    global ats_power_network_stt
    try:
        LOGGER.info('Enter get_state function')
        # read status ats
        # if 'atsConnect' in update_attributes and 'atsContactorGenState' in update_attributes and 'atsContactorElecState' in update_attributes:
        if 'mccSmokeState' in telemetries:
            # is_connect = update_attributes['atsConnect']
            # ats_generator_stt = update_attributes['atsContactorGenState']
            # ats_power_network_stt = update_attributes['atsContactorElecState']
            is_connect = 1
            ats_generator_stt = 0
            ats_power_network_stt = 1
            LOGGER.info('Get information form ats: state')
            return True
        else:
            LOGGER.info('Run to else in get_state function')
            return False
    except Exception as ex:
        LOGGER.info('get_state function error: %s', ex.message)


def get_values_ats():
    global ats_vgen
    global ats_vac
    global ats_vload
    global ats_iload

    try:
        if 'atsVacP1' in telemetries and 'atsVacP2' in telemetries and 'atsVacP3' in telemetries:
            ats_vac = [telemetries['atsVacP1'], telemetries['atsVacP2'], telemetries['atsVacP3']]
            # ats_vgen = [telemetries['atsVgenP1'], telemetries['atsVgenP2'], telemetries['atsVgenP3']]
            # ats_vload = [telemetries['atsVloadP1'], telemetries['atsVloadP2'], telemetries['atsVloadP3']]
            # ats_iload = [telemetries['atsIloadP1'], telemetries['atsIloadP2'], telemetries['atsIloadP3']]
            LOGGER.info('Get information form ats: vol ampe value')
            return True
        else:
            return False
    except Exception as ex:
        LOGGER.info('get_values_ats function error: %s', ex.message)
