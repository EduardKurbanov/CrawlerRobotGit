from typing import Tuple
from ctypes import c_short
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import smbus
import time
import math
from accelerometer_gyroscope_mpu6050 import MPU6050
from compass_magnetometer_hmc5883l import HMC5883L

class Robot(object):
    """
        tracked robot based on a mini computer PocketBeagle®
        model crawler chassis: SN800 19х9х5см
    """
    def __init__(self):
        print('---init ports---')
        self.head_servo_x_pwm = 'P2_1'
        self.head_servo_y_pwm = 'P2_3'
        self.eyes_sonar_trigger_gpio = 'P1_2'
        self.eyes_sonar_echo_gpio = 'P1_4'
        self.engine_standby_gpio = 'P2_2'
        self.engine_right_move_forward_gpio = 'P2_4'
        self.engine_right_move_back_gpio = 'P2_6'
        self.engine_left_move_forward_gpio = 'P2_8'
        self.engine_left_move_back_gpio = 'P2_10'
        #self.i2c_bus = smbus.SMBus(2)


    def servo_head_robot(self, axis_x: float = 0.0, axis_y: float = 0.0) -> str:
        """
           model servo: 'sg90',
           import Adafruit_BBIO.PWM as PWM,
           pwm1 pin: 'P2_1',
           pwm2 pin: 'P2_3',
           axis_x: float: '-90.0 - 0.0 - 90.0',
           axis_y: float: '-90.0 - 0.0 - 90.0',
           :return srt
        """
        print('---init servo_head_robot---')
        duty_min = 5.0
        duty_max = 10.0
        duty_span = duty_max - duty_min

        PWM.start(self.head_servo_x_pwm, (10.0 - duty_min), 30)
        PWM.start(self.head_servo_y_pwm, (10.0 - duty_min), 30)

        duty = ((float(axis_x) / 180.0) * duty_span + duty_min)
        PWM.set_duty_cycle(self.head_servo_x_pwm, duty)
        print(f"angle axis_x {axis_x}")
        duty = ((float(axis_y) / 180.0) * duty_span + duty_min)
        PWM.set_duty_cycle(self.head_servo_y_pwm, duty)
        print(f"angle axis_y {axis_y}")

        if not (-90.0 <= axis_x <= 90.0) or not (-90.0 <= axis_y <= 90.0):
            PWM.stop(self.head_servo_x_pwm) or PWM.stop(self.head_servo_y_pwm)
            PWM.cleanup()
            return f"error angle {axis_x}"

        return "success"

    def eyes_sonar_robot(self) -> float:
        """
            model sonar: 'HY-SRF05' analog 'HY-SR04',
            import Adafruit_BBIO.GPIO as GPIO,
            eyes_sonar_trigger_gpio: 'P1_2'
            eyes_sonar_echo_gpio: 'P1_4',
            :return distance: 'cm'
        """
        print('---init sonar_robot---')
        GPIO.cleanup()
        time.sleep(2)

        print(f"trigger: [{self.eyes_sonar_trigger_gpio}]")
        GPIO.setup(self.eyes_sonar_trigger_gpio, GPIO.OUT)  # Trigger
        print(f"echo: [{self.eyes_sonar_echo_gpio}]")
        GPIO.setup(self.eyes_sonar_echo_gpio, GPIO.IN)  # Echo
        GPIO.output(self.eyes_sonar_trigger_gpio, False)
        print('Setup completed!')
        GPIO.output(self.eyes_sonar_trigger_gpio, False)
        time.sleep(0.5)

        GPIO.output(self.eyes_sonar_trigger_gpio, True)
        time.sleep(0.00001)
        GPIO.output(self.eyes_sonar_trigger_gpio, False)
        pulseStart = time.time()
        pulseEnd = time.time()
        counter = 0

        while GPIO.input(self.eyes_sonar_echo_gpio) == 0:
            pulseStart = time.time()
            counter += 1

        while GPIO.input(self.eyes_sonar_echo_gpio) == 1:
            pulseEnd = time.time()

        pulseDuration = pulseEnd - pulseStart
        distance = pulseDuration * 17150
        distance = round(distance, 2)

        return distance

    def gyroscope_robot(self):
        """
            model gyroscope: L3G4200D
            :return:
        """
        pass

    def gyroscope_accelerometer_robot(self):
        dd = MPU6050()
        pass


    def driver_motor_robot(self, motor_action: str = "") -> None:
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
        print('---init driver_motor_robot---')
        GPIO.cleanup()
        time.sleep(2)
        GPIO.setup(self.engine_standby_gpio, GPIO.OUT)
        GPIO.setup(self.engine_right_move_forward_gpio, GPIO.OUT)
        GPIO.setup(self.engine_right_move_back_gpio, GPIO.OUT)
        GPIO.setup(self.engine_left_move_forward_gpio, GPIO.OUT)
        GPIO.setup(self.engine_left_move_back_gpio, GPIO.OUT)

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

    def module_diagnostics(self):
        pass

    def discharge_controller(self):
        pass





