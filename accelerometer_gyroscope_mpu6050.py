from typing import Tuple, List
from ctypes import c_short
import smbus2
import time
import math


class MPU6050(object):
    """
        for mini computer PocketBeagle®,
        model gyroscope: MPU6050,
        protocol: i2c,
        i2c_pin_sda: 'P1_26'
        i2c_pin_scl: 'P1_28'
    """
    # address MPU-6050 in i2c
    device_address = 0x68
    _WHO_AM_I = 0x75
    # MPU-6050 Registers
    _REGISTER_MPU6050_PWR_MGMT_1 = 0x6B  # Primary power/sleep control register
    _REGISTER_MPU6050_PWR_MGMT_2 = 0x6C  # Secondary power/sleep control register
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

    def __init__(self, i2c: int = 2):
        print('---start_init---')
        self.i2c_bus = smbus2.SMBus(i2c)  # I2C bus number used, may sometimes change on your system
        self.i2c_bus.write_byte_data(self.device_address, self._REGISTER_MPU6050_PWR_MGMT_1, 0x00)  # enable MPU6050
        self.i2c_bus.write_byte_data(self.device_address, self._REGISTER_ACCEL_CONFIG,
                                     self._REGISTER_ACCEL_RANGE_16G)  # set 16g range for accel
        self.i2c_bus.write_byte_data(self.device_address, self._REGISTER_GYRO_CONFIG,
                                     self._REGISTER_GYRO_RANGE_2000DEG)  # set 2000 range for gyro
        time.sleep(1)
        self.gyro_calibration_data: float = []

    def __convert_data_register_shift(self, high_bit=0, low_bit=0):
        high_bit_ = self.i2c_bus.read_byte_data(self.device_address, high_bit)
        low_bit_ = self.i2c_bus.read_byte_data(self.device_address, low_bit)
        signed_int_ = c_short((high_bit_ << 8) | low_bit_).value
        return signed_int_

    def accel_axix_x(self) -> Tuple[float, float]:
        """
        :return: tuple(accel_x, accel_x_gravity)
        """
        signed_int_assel_x = self.__convert_data_register_shift(self._REGISTER_ACCEL_X_OUT_H,
                                                                self._REGISTER_ACCEL_X_OUT_L)
        accel_x = (signed_int_assel_x / self._ACCEL_RANGE_16_G_2048_LSB)
        accel_x_gravity = accel_x * self._STANDARD_GRAVITY
        return (accel_x, accel_x_gravity)

    def accel_axix_y(self) -> Tuple[float, float]:
        """
        :return: tuple(accel_y, accel_y_gravity)
        """
        signed_int_assel_y = self.__convert_data_register_shift(self._REGISTER_ACCEL_Y_OUT_H,
                                                                self._REGISTER_ACCEL_Y_OUT_L)
        accel_y = (signed_int_assel_y / self._ACCEL_RANGE_16_G_2048_LSB)
        accel_y_gravity = accel_y * self._STANDARD_GRAVITY
        return (accel_y, accel_y_gravity)

    def accel_axix_z(self) -> Tuple[float, float]:
        """
        :return: tuple(accel_z, accel_z_gravity)
        """
        signed_int_assel_z = self.__convert_data_register_shift(self._REGISTER_ACCEL_Z_OUT_H,
                                                                self._REGISTER_ACCEL_Z_OUT_L)
        accel_z = (signed_int_assel_z / self._ACCEL_RANGE_16_G_2048_LSB)
        accel_z_gravity = accel_z * self._STANDARD_GRAVITY
        return (accel_z, accel_z_gravity)

    def temp(self) -> float:
        """
        :return: temp
        """
        signed_int_temp = self.__convert_data_register_shift(self._REGISTER_TEMP_OUT_H, self._REGISTER_TEMP_OUT_L)
        temp = ((signed_int_temp) / 340) + 36.53
        return temp

    def gyro_axix_x(self) -> float:
        """
        :return: gyro_x
        """
        signed_int_gyro_x = self.__convert_data_register_shift(self._REGISTER_GYRO_X_OUT_H, self._REGISTER_GYRO_X_OUT_L)
        gyro_x = ((signed_int_gyro_x) / self._GYRO_RANGE_2000_DPS)
        return gyro_x

    def gyro_axix_y(self) -> float:
        """
        :return: gyro_y
        """
        signed_int_gyro_y = self.__convert_data_register_shift(self._REGISTER_GYRO_Y_OUT_H, self._REGISTER_GYRO_Y_OUT_L)
        gyro_y = ((signed_int_gyro_y) / self._GYRO_RANGE_2000_DPS)
        return gyro_y

    def gyro_axix_z(self) -> float:
        """
        :return: gyro_z
        """
        signed_int_gyro_z = self.__convert_data_register_shift(self._REGISTER_GYRO_Z_OUT_H, self._REGISTER_GYRO_Z_OUT_L)
        gyro_z = ((signed_int_gyro_z) / self._GYRO_RANGE_2000_DPS)
        return gyro_z

    def axix_rotation_angle_x(self) -> float:
        """
        :return: axix_rotation_angle_x
        """
        return math.degrees(
            math.atan2(float(self.accel_axix_y()[0]),
                       math.sqrt(float(self.accel_axix_x()[0]) ** 2 + float(self.accel_axix_z()[0]) ** 2)))

    def axix_rotation_angle_y(self) -> float:
        """
        :return: axix_rotation_angle_y
        """
        return math.degrees(
            math.atan2(-float(self.accel_axix_x()[0]),
                       math.sqrt(float(self.accel_axix_y()[0]) ** 2 + float(self.accel_axix_z()[0]) ** 2)))

    def gyro_calibration(self) -> List[float]:
        print("---calibration_gyro---")
        self.gyro_calibration_data: List[float] = [0.0, 0.0, 0.0]

        for _ in range(2000):
            gyro_x = self.gyro_axix_x()
            gyro_y = self.gyro_axix_y()
            gyro_z = self.gyro_axix_z()
            self.gyro_calibration_data[0] += gyro_x
            self.gyro_calibration_data[1] += gyro_y
            self.gyro_calibration_data[2] += gyro_z
            time.sleep(0.01)

        self.gyro_calibration_data = [offset / 2000 for offset in self.gyro_calibration_data]
        print("---calibration_gyro_successfully---")
        return self.gyro_calibration_data


accel_gyro = MPU6050()
g_c = accel_gyro.gyro_calibration()

while True:
    temp = accel_gyro.temp()
    print(f"temp: {temp} C")
    gyro_x = accel_gyro.gyro_axix_x()
    gyro_x -= g_c[0]
    print(f"gyro_x: {gyro_x}")
    time.sleep(0.1)
