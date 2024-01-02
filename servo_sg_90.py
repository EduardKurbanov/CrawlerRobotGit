from typing import Tuple
from ctypes import c_short
import Adafruit_BBIO.PWM as PWM
import time


class SG90(object):
    head_servo_x_pwm = 'P2_1'
    head_servo_y_pwm = 'P2_3'
    __DUTY_MIN = 4.2
    __DUTY_MAX = 12.2
    __DUTY_CONST = 8.2
    __ARR_DATA = []

    def __init__(self):
        print('---init ports sg90---')
        PWM.start(self.head_servo_x_pwm, self.__DUTY_CONST, 50)
        PWM.start(self.head_servo_y_pwm, self.__DUTY_CONST, 50)

    def _set_servo_position(self, pwm_pin, axis_value, sonar):
        if not (-90.0 <= axis_value <= 90.0):
            return f"error angle {axis_value}"
        duty_cycle = self.__DUTY_MIN + (self.__DUTY_MAX - self.__DUTY_MIN) * ((axis_value + 90) / 180.0)
        print(duty_cycle)
        PWM.set_duty_cycle(pwm_pin, duty_cycle)
        tuple_data = (axis_value, sonar)
        self.__ARR_DATA.append(tuple_data)
        return tuple_data

    def servo_axis_x(self, axis_x: float = 0.0, sonar: float = 0.0):
        return self._set_servo_position(self.head_servo_x_pwm, axis_x, sonar)

    def servo_axis_y(self, axis_y: float = 0.0, sonar: float = 0.0):
        return self._set_servo_position(self.head_servo_y_pwm, axis_y, sonar)


# Example usage:
sg90 = SG90()
target_angle_x = 0
sg90.servo_axis_x(target_angle_x)

target_angle_y = 0
sg90.servo_axis_y(target_angle_y)
