from typing import Tuple, List
from ctypes import c_short
import Adafruit_BBIO.PWM as PWM
import time


class SG90(object):
    __DUTY_MIN = 4.2
    __DUTY_MAX = 12.2
    __DUTY_CONST = 8.2
    __ARR_DATA_ANGEL_SONAR = []

    def __init__(self):
        print('---init ports sg90---')
        self.head_servo_x_pwm = 'P2_1'
        self.head_servo_y_pwm = 'P2_3'
        PWM.start(self.head_servo_x_pwm, self.__DUTY_CONST, 50)
        PWM.start(self.head_servo_y_pwm, self.__DUTY_CONST, 50)

    def __set_servo_position(self, pwm_pin, axis_value, sonar) -> Tuple[int, float] or str:
        if not (-90.0 <= axis_value <= 90.0):
            return f"error angle {axis_value}"
        duty_cycle = self.__DUTY_MIN + (self.__DUTY_MAX - self.__DUTY_MIN) * ((axis_value + 90) / 180.0)
        print(duty_cycle)
        PWM.set_duty_cycle(pwm_pin, duty_cycle)
        tuple_data_angle_sonar = (axis_value, sonar)
        self.__ARR_DATA_ANGEL_SONAR.append(tuple_data_angle_sonar)
        return tuple_data_angle_sonar

    def get_data_list_angle_sonar(self) -> List:
        """
        return list -> [(angle, sonar), ...]
        """
        return self.__ARR_DATA_ANGEL_SONAR

    def servo_axis_x(self, axis_x: float = 0.0, sonar: float = 0.0) -> Tuple[int, float] or str:
        """
        return tuple -> (angle, sonar)
        """
        return self.__set_servo_position(self.head_servo_x_pwm, axis_x, sonar)

    def servo_axis_y(self, axis_y: float = 0.0, sonar: float = 0.0) -> Tuple[int, float] or str:
        """
        return tuple -> (angle, sonar)
        """
        return self.__set_servo_position(self.head_servo_y_pwm, axis_y, sonar)


# Example usage:
sg90 = SG90()
target_angle_x = 0
sg90.servo_axis_x(target_angle_x)

target_angle_y = 0
sg90.servo_axis_y(target_angle_y)
