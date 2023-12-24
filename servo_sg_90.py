from typing import Tuple
from ctypes import c_short
import Adafruit_BBIO.PWM as PWM


class SG90(object):
    def __init__(self):
        print('---init ports sg90---')
        self.head_servo_x_pwm = 'P2_1'
        self.head_servo_y_pwm = 'P2_3'

    def servo_axis_x(self, axis_x: float = 0.0) -> str:
        """
           model servo: 'sg90',
           import Adafruit_BBIO.PWM as PWM,
           pwm1 pin: 'P2_1',
           axis_x: float: '-90.0 - 0.0 - 90.0',
           :return srt
        """
        print('---init servo_head_robot---')
        duty_min = 5.0
        duty_max = 10.0
        duty_span = duty_max - duty_min

        PWM.start(self.head_servo_x_pwm, (10.0 - duty_min), 30)

        duty = ((float(axis_x) / 180.0) * duty_span + duty_min)
        PWM.set_duty_cycle(self.head_servo_x_pwm, duty)
        print(f"angle axis_x {axis_x}")

        if not (-90.0 <= axis_x <= 90.0):
            PWM.stop(self.head_servo_x_pwm)
            PWM.cleanup()
            return f"error angle {axis_x}"

        return "success"

    def servo_axis_y(self, axis_x: float = 0.0, axis_y: float = 0.0) -> str:
        """
           model servo: 'sg90',
           import Adafruit_BBIO.PWM as PWM,
           pwm2 pin: 'P2_3',
           axis_y: float: '-90.0 - 0.0 - 90.0',
           :return srt
        """
        print('---init servo_head_robot---')
        duty_min = 5.0
        duty_max = 10.0
        duty_span = duty_max - duty_min

        PWM.start(self.head_servo_y_pwm, (10.0 - duty_min), 30)

        duty = ((float(axis_y) / 180.0) * duty_span + duty_min)
        PWM.set_duty_cycle(self.head_servo_y_pwm, duty)
        print(f"angle axis_y {axis_y}")

        if not (-90.0 <= axis_x <= 90.0):
            PWM.stop(self.head_servo_y_pwm)
            PWM.cleanup()
            return f"error angle {axis_y}"

        return "success"
