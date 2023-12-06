from typing import Tuple
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import smbus
import time

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
        device_address = 0x68
        _MPU6050_PWR_MGMT_1 = 0x6B  # Primary power/sleep control register
        _MPU6050_PWR_MGMT_2 = 0x6C
        _ACCEL_X_OUT_H = 0x3B
        _ACCEL_X_OUT_L = 0x3C
        _ACCEL_Y_OUT_H = 0x3D
        _ACCEL_Y_OUT_L = 0x3E
        _ACCEL_Z_OUT_H = 0x3F
        _ACCEL_Z_OUT_L = 0x40
        _TEMP_OUT_H = 0X41
        _TEMP_OUT_L = 0X42
        _GYRO_X_OUT_H = 0x43
        _GYRO_X_OUT_L = 0x44
        _GYRO_Y_OUT_H = 0x45
        _GYRO_Y_OUT_L = 0x46
        _GYRO_Z_OUT_H = 0x47
        _GYRO_Z_OUT_L = 0x48
        _STANDARD_GRAVITY = 9.80665

        _RANGE_2_G_16384_LSB = 16384  # +/- 2g (default value), 16384 LSB/G (default value)
        _RANGE_4_G_8192_LSB = 8192  # +/- 4g, 8192 LSB/G
        _RANGE_8_G_4096_LSB = 4096  # +/- 8g, 4096 LSB/G
        _RANGE_16_G_2048_LSB = 2048  # +/- 16g, 2048 LSB/G

        _RANGE_250_DPS = 131  # +/- 250 deg/s (default value)
        _RANGE_500_DPS = 65.5  # +/- 500 deg/s
        _RANGE_1000_DPS = 32.8  # +/- 1000 deg/s
        _RANGE_2000_DPS = 16.4  # +/- 2000 deg/s

        bus = smbus.SMBus(2)  # The I2C bus number used may need to be changed on your system
        bus.write_byte_data(device_address, _MPU6050_PWR_MGMT_1, 0)  # Enabling MPU6050
        time.sleep(1)

        accel_x_h = bus.read_byte_data(device_address, _ACCEL_X_OUT_H)
        accel_x_l = bus.read_byte_data(device_address, _ACCEL_X_OUT_L)
        assel_x_hex_bit = (accel_x_h << 8) | accel_x_l
        signed_hex_assel_x = (int(hex(assel_x_hex_bit), 16) + 2 ** 15) % 2 ** 16 - 2 ** 15
        accel_x = (signed_hex_assel_x / _RANGE_4_G_8192_LSB) * _STANDARD_GRAVITY

        accel_y_h = bus.read_byte_data(device_address, _ACCEL_Y_OUT_H)
        accel_y_l = bus.read_byte_data(device_address, _ACCEL_Y_OUT_L)
        assel_y_hex_bit = (accel_y_h << 8) | accel_y_l
        signed_hex_assel_y = (int(hex(assel_y_hex_bit), 16) + 2 ** 15) % 2 ** 16 - 2 ** 15
        accel_y = (signed_hex_assel_y / _RANGE_4_G_8192_LSB) * _STANDARD_GRAVITY

        accel_z_h = bus.read_byte_data(device_address, _ACCEL_Z_OUT_H)
        accel_z_l = bus.read_byte_data(device_address, _ACCEL_Z_OUT_L)
        assel_z_hex_bit = (accel_z_h << 8) | accel_z_l
        signed_hex_assel_z = (int(hex(assel_z_hex_bit), 16) + 2 ** 15) % 2 ** 16 - 2 ** 15
        accel_z = (signed_hex_assel_z / _RANGE_4_G_8192_LSB) * _STANDARD_GRAVITY

        temp_hex_h = bus.read_byte_data(device_address, _TEMP_OUT_H)
        temp_hex_l = bus.read_byte_data(device_address, _TEMP_OUT_L)
        temp_hex_bit = (temp_hex_h << 8) | temp_hex_l
        signed_hex_temp = (int(hex(temp_hex_bit), 16) + 2 ** 15) % 2 ** 16 - 2 ** 15
        temp = ((signed_hex_temp) / 340) + 36.53

        gyro_x_h = bus.read_byte_data(device_address, _GYRO_X_OUT_H)
        gyro_x_l = bus.read_byte_data(device_address, _GYRO_X_OUT_L)
        gyro_x_hex_bit = (gyro_x_h << 8) | gyro_x_l
        signed_hex_gyro_x = (int(hex(gyro_x_hex_bit), 16) + 2 ** 15) % 2 ** 16 - 2 ** 15
        gyro_x = ((signed_hex_gyro_x) / _RANGE_500_DPS)

        gyro_y_h = bus.read_byte_data(device_address, _GYRO_Y_OUT_H)
        gyro_y_l = bus.read_byte_data(device_address, _GYRO_Y_OUT_L)
        gyro_y_hex_bit = (gyro_y_h << 8) | gyro_y_l
        signed_hex_gyro_y = (int(hex(gyro_y_hex_bit), 16) + 2 ** 15) % 2 ** 16 - 2 ** 15
        gyro_y = ((signed_hex_gyro_y) / _RANGE_500_DPS)

        gyro_z_h = bus.read_byte_data(device_address, _GYRO_Z_OUT_H)
        gyro_z_l = bus.read_byte_data(device_address, _GYRO_Z_OUT_L)
        gyro_z_hex_bit = (gyro_z_h << 8) | gyro_z_l
        signed_hex_gyro_z = (int(hex(gyro_z_hex_bit), 16) + 2 ** 15) % 2 ** 16 - 2 ** 15
        gyro_z = ((signed_hex_gyro_z) / _RANGE_500_DPS)

        return (accel_x, accel_y, accel_z, temp, gyro_x, gyro_y, gyro_z)

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



