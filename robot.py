from typing import Tuple
from ctypes import c_short
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import smbus
import time
import math

class Robot:
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
        self.i2c_bus = smbus.SMBus(2)


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

    def gyroscope_accelerometer_robot(self) -> Tuple[float, float, float, float, float, float, float]:
        """
            model gyroscope: MPU6050,
            protocol: i2c,
            i2c_pin_sda: 'P1_26'
            i2c_pin_scl: 'P1_28'
            :return: (accel_x, accel_y, accel_x, temp, gyro_x, gyro_y, gyro_z),
        """
        # address MPU-6050 in i2c
        device_address = 0x68
        # MPU-6050 Registers
        _REGISTER_MPU6050_PWR_MGMT_1 = 0x6B  # Primary power/sleep control register
        _REGISTER_MPU6050_PWR_MGMT_2 = 0x6C
        _REGISTER_GYRO_CONFIG = 0x1B
        _REGISTER_ACCEL_CONFIG = 0x1C
        _REGISTER_ACCEL_X_OUT_H = 0x3B
        _REGISTER_ACCEL_X_OUT_L = 0x3C
        _REGISTER_ACCEL_Y_OUT_H = 0x3D
        _REGISTER_ACCEL_Y_OUT_L = 0x3E
        _REGISTER_ACCEL_Z_OUT_H = 0x3F
        _REGISTER_ACCEL_Z_OUT_L = 0x40
        _REGISTER_TEMP_OUT_H = 0X41
        _REGISTER_TEMP_OUT_L = 0X42
        _REGISTER_GYRO_X_OUT_H = 0x43
        _REGISTER_GYRO_X_OUT_L = 0x44
        _REGISTER_GYRO_Y_OUT_H = 0x45
        _REGISTER_GYRO_Y_OUT_L = 0x46
        _REGISTER_GYRO_Z_OUT_H = 0x47
        _REGISTER_GYRO_Z_OUT_L = 0x48
        # Pre-defined ranges
        _REGISTER_ACCEL_RANGE_2G = 0x00
        _REGISTER_ACCEL_RANGE_4G = 0x08
        _REGISTER_ACCEL_RANGE_8G = 0x10
        _REGISTER_ACCEL_RANGE_16G = 0x18
        _REGISTER_GYRO_RANGE_250DEG = 0x00
        _REGISTER_GYRO_RANGE_500DEG = 0x08
        _REGISTER_GYRO_RANGE_1000DEG = 0x10
        _REGISTER_GYRO_RANGE_2000DEG = 0x18
        # earth gravity
        _STANDARD_GRAVITY = 9.80665
        # Modifiers accel
        _ACCEL_RANGE_2_G_16384_LSB = 16384.0  # +/- 2g (default value), 16384 LSB/G (default value)
        _ACCEL_RANGE_4_G_8192_LSB = 8192.0  # +/- 4g, 8192 LSB/G
        _ACCEL_RANGE_8_G_4096_LSB = 4096.0  # +/- 8g, 4096 LSB/G
        _ACCEL_RANGE_16_G_2048_LSB = 2048.0  # +/- 16g, 2048 LSB/G
        # Modifiers gyro
        _GYRO_RANGE_250_DPS = 131.0  # +/- 250 deg/s (default value)
        _GYRO_RANGE_500_DPS = 65.5  # +/- 500 deg/s
        _GYRO_RANGE_1000_DPS = 32.8  # +/- 1000 deg/s
        _GYRO_RANGE_2000_DPS = 16.4  # +/- 2000 deg/s

        bus = self.i2c_bus  # I2C bus number used, may sometimes change on your system
        bus.write_byte_data(device_address, _REGISTER_MPU6050_PWR_MGMT_1, 0x00)  # enable MPU6050
        bus.write_byte_data(device_address, _REGISTER_ACCEL_CONFIG, _REGISTER_ACCEL_RANGE_16G)  # set 16g range for accel
        bus.write_byte_data(device_address, _REGISTER_GYRO_CONFIG, _REGISTER_GYRO_RANGE_2000DEG)  # set 2000 range for gyro
        time.sleep(1)

        accel_x_h = bus.read_byte_data(device_address, _REGISTER_ACCEL_X_OUT_H)
        accel_x_l = bus.read_byte_data(device_address, _REGISTER_ACCEL_X_OUT_L)
        signed_int_assel_x = c_short((accel_x_h << 8) | accel_x_l).value
        accel_x = (signed_int_assel_x / _ACCEL_RANGE_16_G_2048_LSB)
        accel_x_gravity = accel_x * _STANDARD_GRAVITY

        accel_y_h = bus.read_byte_data(device_address, _REGISTER_ACCEL_Y_OUT_H)
        accel_y_l = bus.read_byte_data(device_address, _REGISTER_ACCEL_Y_OUT_L)
        signed_int_assel_y = c_short((accel_y_h << 8) | accel_y_l).value
        accel_y = (signed_int_assel_y / _ACCEL_RANGE_16_G_2048_LSB)
        accel_y_gravity = accel_y * _STANDARD_GRAVITY

        accel_z_h = bus.read_byte_data(device_address, _REGISTER_ACCEL_Z_OUT_H)
        accel_z_l = bus.read_byte_data(device_address, _REGISTER_ACCEL_Z_OUT_L)
        signed_int_assel_z = c_short((accel_z_h << 8) | accel_z_l).value
        accel_z = (signed_int_assel_z / _ACCEL_RANGE_16_G_2048_LSB)
        accel_z_gravity = accel_z * _STANDARD_GRAVITY

        temp_hex_h = bus.read_byte_data(device_address, _REGISTER_TEMP_OUT_H)
        temp_hex_l = bus.read_byte_data(device_address, _REGISTER_TEMP_OUT_L)
        signed_int_temp = c_short((temp_hex_h << 8) | temp_hex_l).value
        temp = ((signed_int_temp) / 340) + 36.53

        gyro_x_h = bus.read_byte_data(device_address, _REGISTER_GYRO_X_OUT_H)
        gyro_x_l = bus.read_byte_data(device_address, _REGISTER_GYRO_X_OUT_L)
        signed_int_gyro_x = c_short((gyro_x_h << 8) | gyro_x_l).value
        gyro_x = ((signed_int_gyro_x) / _GYRO_RANGE_2000_DPS)

        gyro_y_h = bus.read_byte_data(device_address, _REGISTER_GYRO_Y_OUT_H)
        gyro_y_l = bus.read_byte_data(device_address, _REGISTER_GYRO_Y_OUT_L)
        signed_int_gyro_y = c_short((gyro_y_h << 8) | gyro_y_l).value
        gyro_y = ((signed_int_gyro_y) / _GYRO_RANGE_2000_DPS)

        gyro_z_h = bus.read_byte_data(device_address, _REGISTER_GYRO_Z_OUT_H)
        gyro_z_l = bus.read_byte_data(device_address, _REGISTER_GYRO_Z_OUT_L)
        signed_int_gyro_z = c_short((gyro_z_h << 8) | gyro_z_l).value
        gyro_z = ((signed_int_gyro_z) / _GYRO_RANGE_2000_DPS)

        axix_rotation_angle_x = math.degrees(
            math.atan2(float(accel_y), math.sqrt(float(accel_x) ** 2 + float(accel_z) ** 2)))

        axix_rotation_angle_y = math.degrees(
            math.atan2(-float(accel_x), math.sqrt(float(accel_y) ** 2 + float(accel_z) ** 2)))

        return (accel_x_gravity, accel_y_gravity, accel_z_gravity, temp, gyro_x, gyro_y, gyro_z, axix_rotation_angle_x,
                axix_rotation_angle_y)


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



