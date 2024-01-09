from typing import Tuple
from ctypes import c_short
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time


class DVR8833(object):
    def __init__(self):
        print('---init ports dvr8833---')
        self.engine_standby_gpio = 'P2_6'
        self.engine_right_move_forward_gpio = 'P2_4'
        self.engine_right_move_back_gpio = 'P2_2'
        self.engine_left_move_forward_gpio = 'P2_8'
        self.engine_left_move_back_gpio = 'P2_10'
        self.__gpio_init_driver_motor()

    def __gpio_init_driver_motor(self):
        print('---init driver_motor_robot---')
        #GPIO.cleanup()
        #time.sleep(0.1)
        GPIO.setup(self.engine_standby_gpio, GPIO.OUT)
        GPIO.setup(self.engine_right_move_forward_gpio, GPIO.OUT)
        GPIO.setup(self.engine_right_move_back_gpio, GPIO.OUT)
        GPIO.setup(self.engine_left_move_forward_gpio, GPIO.OUT)
        GPIO.setup(self.engine_left_move_back_gpio, GPIO.OUT)

    def driver_motor(self, motor_action: str = "") -> None:
        """
            model driver motor: 'DRV8833'
            import Adafruit_BBIO.GPIO as GPIO,
            engine_standby_gpio = 'P2_2',
            engine_right_move_forward_gpio = 'P2_4',
            engine_right_move_back_gpio = 'P2_6',
            engine_left_move_forward_gpio = 'P2_8',
            engine_left_move_back_gpio = 'P2_10',
            motor_action: str: 'forward or back or left or stop',
            :return None:
        """

        if motor_action == 'forward':
            print('---motors forward---')
            GPIO.output(self.engine_standby_gpio, GPIO.HIGH)

            (GPIO.output(self.engine_right_move_forward_gpio, GPIO.HIGH) and
             GPIO.output(self.engine_right_move_back_gpio, GPIO.LOW))

            (GPIO.output(self.engine_left_move_forward_gpio, GPIO.HIGH) and
             GPIO.output(self.engine_left_move_back_gpio, GPIO.LOW))
        elif motor_action == 'back':
            print('---motors back---')
            GPIO.output(self.engine_standby_gpio, GPIO.HIGH)

            (GPIO.output(self.engine_right_move_forward_gpio, GPIO.LOW) and
             GPIO.output(self.engine_right_move_back_gpio, GPIO.HIGH))

            (GPIO.output(self.engine_left_move_forward_gpio, GPIO.LOW) and
             GPIO.output(self.engine_left_move_back_gpio, GPIO.HIGH))
        elif motor_action == 'right':
            print('---motors right---')
            GPIO.output(self.engine_standby_gpio, GPIO.HIGH)

            (GPIO.output(self.engine_left_move_forward_gpio, GPIO.HIGH) and
             GPIO.output(self.engine_left_move_back_gpio, GPIO.LOW))
        elif motor_action == 'left':
            print('---motors left---')
            GPIO.output(self.engine_standby_gpio, GPIO.HIGH)

            (GPIO.output(self.engine_right_move_forward_gpio, GPIO.HIGH) and
             GPIO.output(self.engine_right_move_back_gpio, GPIO.LOW))
        elif motor_action == 'stop':
            print('stop motor')
            GPIO.output(self.engine_standby_gpio, GPIO.LOW)
            GPIO.cleanup()
        else:
            print('---error command, off standby---')
            GPIO.output(self.engine_standby_gpio, GPIO.LOW)
            GPIO.cleanup()
