import Adafruit_BBIO.GPIO as GPIO
import time


class Alert(object):
    def __init__(self):
        self.__sound_signal_buzzer = 'P2_31'
        self.__power_line_switch_9v = 'P2_9'
        self.__left_motor_power_outputA1_9v = 'P2_20'
        self.__right_motor_power_outputA1_9v = 'P2_18'

    def disconnecting_the_power_line_9v(self, power_control: float):
        pass

    def beep_error_code(self):
        pass