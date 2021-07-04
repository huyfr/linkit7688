import time

from config import *
from config.common import *

CONTINUOUS_RUN = 180 * 60  # time run
acm_period_start = 0
acm_air_alter_state = True
acm_air_alter_time = 0


def _send_command(command):
    commands_lock.acquire()
    commands[DEVICE_ACM] = command
    commands_lock.release()
    return DEVICE_ACM + ':' + command


# This method is called every loop if the device is in Auto mode
def check_status():
    LOGGER.info('Enter monitor:acm:check_status')
    global acm_period_start
    global acm_air_alter_state
    global acm_air_alter_time

    # Time to run in alternative mode (not used), convert from hour to second
    acmAlternativeTime = 3600 * shared_attributes.get('acmAlternativeTime', default_data.acmAlternativeTime)
    # Time to run/rest air-conditioner if T is lower than T2, , convert from hour to second
    acmRunTime = 3600 * shared_attributes.get('acmRunTime', default_data.acmRunTime)
    acmRestTime = 3600 * shared_attributes.get('acmRestTime', default_data.acmRestTime)
    acmGenAllow = shared_attributes.get('acmGenAllow', default_data.acmGenAllow)
    acmVacThreshold = shared_attributes.get('acmVacThreshold', default_data.acmVacThreshold)
    # acmMinHumid = shared_attributes.get('acmMinHumid', default_data.acmMinHumid)
    acmMaxHumid = shared_attributes.get('acmMaxHumid', default_data.acmMaxHumid)
    # acmExpectedTemp = shared_attributes.get('acmExpectedTemp', default_data.acmExpectedTemp)
    # acmExpectedHumid = shared_attributes.get('acmExpectedHumid', default_data.acmExpectedHumid)
    acmT1Temp = shared_attributes.get('acmT1Temp', default_data.acmT1Temp)
    acmT2Temp = shared_attributes.get('acmT2Temp', default_data.acmT2Temp)
    acmT3Temp = shared_attributes.get('acmT3Temp', default_data.acmT3Temp)
    acmT4Temp = shared_attributes.get('acmT4Temp', default_data.acmT4Temp)

    # Client
    acmOnlineState = client_attributes.get('acmOnlineState', default_data.acmOnlineState)
    # acmAutoMode = client_attributes.get('acmAutoMode', default_data.acmAutoMode)
    # acmTempError = client_attributes.get('acmTempError', default_data.acmTempError)
    # acmHumidError = client_attributes.get('acmHumidError', default_data.acmHumidError)
    # acmIState = client_attributes.get('acmIState', default_data.acmIState)
    acmAirc1RunState = client_attributes.get('acmAirc1RunState', default_data.acmAirc1RunState)
    acmAirc2RunState = client_attributes.get('acmAirc2RunState', default_data.acmAirc2RunState)
    # acmAirc1Error = client_attributes.get('acmAirc1Error', default_data.acmAirc1Error)
    # acmAirc2Error = client_attributes.get('acmAirc2Error', default_data.acmAirc2Error)
    acmFanRunState = client_attributes.get('acmFanRunState', default_data.acmFanRunState)
    # acmFanError = client_attributes.get('acmFanError', default_data.acmFanError)

    # Telemetry
    acmTempIndoor = telemetries.get('acmTempIndoor', default_data.acmTempIndoor)
    acmTempOutdoor = telemetries.get('acmTempOutdoor', default_data.acmTempOutdoor)
    acmHumidIndoor = telemetries.get('acmHumidIndoor', default_data.acmHumidIndoor)
    # acmT1TempUser = telemetries.get('acmT1Temp', default_data.acmT1Temp)
    # acmT2TempUser = telemetries.get('acmT2Temp', default_data.acmT2Temp)
    # acmT3TempUser = telemetries.get('acmT3Temp', default_data.acmT3Temp)
    # acmT4TempUser = telemetries.get('acmT4Temp', default_data.acmT4Temp)

    mccSmokeState = telemetries.get('mccSmokeState', default_data.mccSmokeState)
    mccFireState = telemetries.get('mccFireState', default_data.mccFireState)

    atsAcState = client_attributes.get('atsAcState', default_data.atsAcState)

    atsVacP1 = telemetries.get('atsVacP1', default_data.atsVacP1)
    atsVacP2 = telemetries.get('atsVacP2', default_data.atsVacP2)
    atsVacP3 = telemetries.get('atsVacP3', default_data.atsVacP3)
    atsVgenP1 = telemetries.get('atsVgenP1', default_data.atsVgenP1)
    atsVgenP2 = telemetries.get('atsVgenP2', default_data.atsVgenP2)
    atsVgenP3 = telemetries.get('atsVgenP3', default_data.atsVgenP3)

    atsContactorElecState = client_attributes.get('atsContactorElecState', default_data.atsContactorElecState)
    atsContactorGenState = client_attributes.get('atsContactorGenState', default_data.atsContactorGenState)

    # Get current time
    timestamp = time.time()
    if acm_air_alter_time == 0:
        acm_air_alter_time = timestamp

    TempDelta = 1   # Delta temperature (in Celcius degree)

    # Decide whether to run air or fan
    air_enabled = True

    acmAirc1NextState = acmAirc1CurrentState = (acmAirc1RunState == 1)
    acmAirc2NextState = acmAirc2CurrentState = (acmAirc2RunState == 1)
    acmFanCurrentState = acmFanNextState = (acmFanRunState == 1)

    '''
    Running Permission
    '''
    # Run air-conditioner with power-generator
    # atsAcState: Lost AC Grid
    if acmGenAllow == 0 and atsAcState == 0:
        LOGGER.debug('# On power-generator, don\'t run AIRC')
        air_enabled = False

    # Don't run air-conditioner if low AC
    # TODO: make sure all BTS have 3-phase AC
    # if atsContactorElecState == 1 and (atsVacP1 < acmVacThreshold
    #                                    or atsVacP2 < acmVacThreshold
    #                                    or atsVacP3 < acmVacThreshold) \
    #         or atsContactorGenState == 1 and (atsVgenP1 < acmVacThreshold
    #                                           or atsVgenP2 < acmVacThreshold
    #                                           or atsVgenP3 < acmVacThreshold):
    #     LOGGER.debug('# Low AC, don\'t run AIRC')
    #     air_enabled = False

    '''
    Auto procedure, High -> Low priority:
    '''
    if mccSmokeState == 1 or mccFireState == 1:
        # Force turn off air-conditioner & fan when in fire
        LOGGER.debug('# Smoke or fire detected, turn off AIRC & FAN')
        acmAirc1NextState = False
        acmAirc2NextState = False
        acmFanNextState = False
        acm_period_start = 0    # Reset period timer
        acm_air_alter_time = timestamp
    elif acmHumidIndoor > acmMaxHumid:
        # When too humid, must turn on air-conditioner, turn off fan, don't care for temperature
        LOGGER.debug('# Humidity too high, turn on AIRC, turn off FAN')
        # But it won't run if power is too low or on Gen or Batt
        acmAirc1NextState = air_enabled
        acmAirc2NextState = air_enabled
        acmFanNextState = False
        acm_period_start = 0    # Reset period timer
        acm_air_alter_time = timestamp
    elif acmTempIndoor > acmT1Temp:
        # Temperature driven: T > T1 ~ run both Air if enabled
        LOGGER.debug('# Temperature driven: T > T1 ~ run both Air if enabled')
        acmAirc1NextState = air_enabled
        acmAirc2NextState = air_enabled
        acmFanNextState = False
        acm_period_start = 0    # Reset period timer
        acm_air_alter_time = timestamp
    elif acmT2Temp < acmTempIndoor < acmT1Temp - TempDelta:
        # Temperature driven: T1 - TempDelta > T > T2 ~ run only one Air if enabled
        LOGGER.debug('# Temperature driven: T1 - TempDelta > T > T2'
                     ' => run only one Air if enabled')
        acmAirc1NextState = air_enabled and acm_air_alter_state
        acmAirc2NextState = air_enabled and not acm_air_alter_state
        acmFanNextState = False
        acm_period_start = 0    # Reset period timer
    elif acmTempIndoor < acmT2Temp - TempDelta:
        # Fan should already be enabled
        if acmTempOutdoor > acmT4Temp + TempDelta:
            # If temp_outdoor > T4 + delta => always one Air
            LOGGER.debug('# If temp_outdoor > T4 + delta => always one Air')
            acmAirc1NextState = air_enabled and acm_air_alter_state
            acmAirc2NextState = air_enabled and not acm_air_alter_state
            acmFanNextState = False
        elif acmTempOutdoor < acmT4Temp:
            # If temp_outdoor < T4 => Air off for t1 (Fan only), after t1 if temp_indoor > T3 => Air in t2 time
            LOGGER.debug('# If temp_outdoor < T4 => Air off for t1 (Fan only), after t1 if temp_indoor > T3'
                         ' => Air in t2 time')
            # t1 = acmRestTime
            # t2 = acmRunTime
            period_elapsed = timestamp - acm_period_start     # time since start of current period (either Running or Resting)
            if (not acmAirc1CurrentState and not acmAirc2CurrentState) and \
                    period_elapsed > acmRestTime and \
                    acmTempIndoor > acmT3Temp:
                # Currently in Resting period (Fan only) while t1 is due and temp_indoor is higher than T3
                # => Run arc1 in t2 time (start a new period)
                LOGGER.debug('# Resting => Run arc1 in t2 time (start a new period)')
                acm_period_start = timestamp
                acmAirc1NextState = air_enabled and acm_air_alter_state
                acmAirc2NextState = air_enabled and not acm_air_alter_state
                acmFanNextState = False
            elif (acmAirc1CurrentState or acmAirc2CurrentState) and \
                    period_elapsed > acmRunTime and \
                    acmTempIndoor < acmT3Temp:
                # Currently in Running period (1 Air) while t2 is due and temp_indoor is expected (lower than T3)
                # => Stop Air, run only fan in t1 time (start a new period)
                LOGGER.debug('# Running => Stop Air, run only fan in t1 time (start a new period)')
                acm_period_start = timestamp
                acm_air_alter_time = timestamp
                acmAirc1NextState = False
                acmAirc2NextState = False
                acmFanNextState = True

    # Counting alternative time, only if 1 airc is running:
    if (acmAirc1NextState and not acmAirc2NextState) or (not acmAirc1NextState and acmAirc2NextState):
        # Set acmAlternativeTime to = to disable alternative mode
        if timestamp - acm_air_alter_time > acmAlternativeTime > 0:
            acm_air_alter_time = timestamp
            acm_air_alter_state = not acm_air_alter_state

    if not acmOnlineState:
        LOGGER.debug("ACM not online, won't send command")
        return ''

    '''
    Checking next state and issue command
    '''
    rtn = ''
    if acmAirc1CurrentState and not acmAirc1NextState:
        rtn += _send_command(COMMAND_ACM_AIRC_1_OFF) + ' | '
    if not acmAirc1CurrentState and acmAirc1NextState:
        rtn += _send_command(COMMAND_ACM_AIRC_1_ON) + ' | '
    if acmAirc2CurrentState and not acmAirc2NextState:
        rtn += _send_command(COMMAND_ACM_AIRC_2_OFF) + ' | '
    if not acmAirc2CurrentState and acmAirc2NextState:
        rtn += _send_command(COMMAND_ACM_AIRC_2_ON) + ' | '
    if acmFanCurrentState and not acmFanNextState:
        rtn += _send_command(COMMAND_ACM_FAN_OFF) + ' | '
    if not acmFanCurrentState and acmFanNextState:
        rtn += _send_command(COMMAND_ACM_FAN_ON) + ' | '

    LOGGER.info('Exit monitor:acm:check_status - ' + rtn)
    return rtn
