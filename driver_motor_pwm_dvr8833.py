from typing import Tuple
from ctypes import c_short
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time


class DVR8833(object):
    def __init__(self):
        print('---init ports dvr8833---')
        self.engine_standby_gpio = 'P1_35'
        self.engine_right_move_forward_gpio_pwm_a = 'P1_36'
        self.engine_right_move_back_gpio = '1_29'
        self.engine_left_move_forward_gpio_pwm_b = 'P1_33'
        self.engine_left_move_back_gpio = 'P1_31'
        self.frequency_pwm = 15000
        self.duty_cycle_pwm = 100
        self.polarity_pwm_0 = 0
        self.polarity_pwm_1 = 1
        self.__DUTY_CYCLE_PWM_BACK = 0

    def driver_motor(self, motor_action: str = "", duty_cycle: float = 0) -> None:
        """
            model driver motor: 'DRV8833'
            import Adafruit_BBIO.GPIO as GPIO,
            engine_standby_gpio = 'P1_35',
            engine_right_move_forward_gpio_pwm_a = 'P1_36',
            engine_right_move_back_gpio = 'P1_29',
            engine_left_move_forward_gpio_pwm_b = 'P1_33',
            engine_left_move_back_gpio = 'P1_31',
            motor_action: str: 'forward or back or left or stop',
            duty_cycle: float: 50 > 100 %
            :return None:
        """
        print('---init driver_motor_robot---')
        GPIO.cleanup()
        time.sleep(2)
        GPIO.setup(self.engine_standby_gpio, GPIO.OUT)
        GPIO.setup(self.engine_right_move_back_gpio, GPIO.OUT)
        GPIO.setup(self.engine_left_move_back_gpio, GPIO.OUT)
        PWM.start(self.engine_left_move_forward_gpio_pwm_b, self.duty_cycle_pwm, self.frequency_pwm,
                  self.polarity_pwm_1)
        PWM.start(self.engine_right_move_forward_gpio_pwm_a, self.duty_cycle_pwm, self.frequency_pwm,
                  self.polarity_pwm_1)

        if motor_action == 'forward':
            print('---motors forward---')
            GPIO.output(self.engine_standby_gpio, GPIO.HIGH)

            (PWM.set_duty_cycle(self.engine_left_move_forward_gpio_pwm_b, duty_cycle) and
             GPIO.output(self.engine_right_move_back_gpio, GPIO.LOW))

            (PWM.set_duty_cycle(self.engine_right_move_forward_gpio_pwm_a, duty_cycle) and
             GPIO.output(self.engine_left_move_back_gpio, GPIO.LOW))
        elif motor_action == 'back':
            print('---motors back---')
            GPIO.output(self.engine_standby_gpio, GPIO.HIGH)

            (PWM.set_duty_cycle(self.engine_right_move_forward_gpio_pwm_a, self.__DUTY_CYCLE_PWM_BACK) and
             GPIO.output(self.engine_right_move_back_gpio, GPIO.HIGH))

            (PWM.set_duty_cycle(self.engine_left_move_forward_gpio_pwm_b, self.__DUTY_CYCLE_PWM_BACK) and
             GPIO.output(self.engine_left_move_back_gpio, GPIO.HIGH))
        elif motor_action == 'right':
            print('---motors right---')
            GPIO.output(self.engine_standby_gpio, GPIO.HIGH)

            (PWM.set_duty_cycle(self.engine_left_move_forward_gpio_pwm_b, duty_cycle) and
             GPIO.output(self.engine_left_move_back_gpio, GPIO.LOW))
        elif motor_action == 'left':
            print('---motors left---')
            GPIO.output(self.engine_standby_gpio, GPIO.HIGH)

            (PWM.set_duty_cycle(self.engine_right_move_forward_gpio_pwm_a, duty_cycle) and
             GPIO.output(self.engine_right_move_back_gpio, GPIO.LOW))
        elif motor_action == 'stop':
            print('stop motor')
            GPIO.output(self.engine_standby_gpio, GPIO.LOW)
            GPIO.cleanup()
            PWM.stop(self.engine_right_move_forward_gpio_pwm_a)
            PWM.stop(self.engine_left_move_forward_gpio_pwm_b)
            PWM.cleanup()
        else:
            print('---error command, off standby---')
            GPIO.output(self.engine_standby_gpio, GPIO.LOW)
            GPIO.cleanup()
            PWM.stop(self.engine_right_move_forward_gpio_pwm_a)
            PWM.stop(self.engine_left_move_forward_gpio_pwm_b)
            PWM.cleanup()
