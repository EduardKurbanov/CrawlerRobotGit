from typing import Tuple
from ctypes import c_short
import Adafruit_BBIO.PWM as PWM
import time


class SG90(object):
    def __init__(self):
        self.head_servo_x_pwm = 'P2_1'
        self.head_servo_y_pwm = 'P2_3'
        self.duty_min = 5.0
        self.duty_max = 10.0
        self.step_size = 1
        self.delay = 0.05

        print('---init ports sg90---')
        PWM.start(self.head_servo_x_pwm, (10.0 - self.duty_min), 30)
        PWM.start(self.head_servo_y_pwm, (10.0 - self.duty_min), 30)

    def _set_servo_position(self, pwm_pin, axis_value, axis_name):
        duty_span = self.duty_max - self.duty_min
        duty = ((float(axis_value) / 180.0) * duty_span + self.duty_min)
        PWM.set_duty_cycle(pwm_pin, duty)

        calculated_angle = ((duty - self.duty_min) / duty_span) * 180.0

        if not (-90.0 <= axis_value <= 90.0):
            PWM.stop(pwm_pin)
            PWM.cleanup()
            return f"error angle {axis_value}"

        return calculated_angle

    def _smooth_rotate(self, pwm_pin, current_angle, target_angle):
        direction = 1 if target_angle > current_angle else -1
        for angle in range(int(current_angle), int(target_angle) + direction, direction * self.step_size):
            self._set_servo_position(pwm_pin, angle, pwm_pin)
            print(f"Servo {pwm_pin}: Target Angle: {target_angle}, Current Angle: {angle}")
            time.sleep(self.delay)

        return self._set_servo_position(pwm_pin, target_angle, pwm_pin)

    def servo_axis_x(self, target_angle_x: float = 0.0):
        current_angle_x = self._set_servo_position(self.head_servo_x_pwm, 0, 'axis_x')
        return self._smooth_rotate(self.head_servo_x_pwm, current_angle_x, target_angle_x)

    def servo_axis_y(self, target_angle_y: float = 0.0):
        current_angle_y = self._set_servo_position(self.head_servo_y_pwm, 0, 'axis_y')
        return self._smooth_rotate(self.head_servo_y_pwm, current_angle_y, target_angle_y)


# Example usage:
sg90 = SG90()
target_angle_x = 0
sg90.servo_axis_x(target_angle_x)

target_angle_y = 0
sg90.servo_axis_y(target_angle_y)
