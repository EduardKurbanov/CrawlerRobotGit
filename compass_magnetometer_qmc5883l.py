from typing import Tuple, List
from ctypes import c_short
import smbus2
import time
import math


class QMC5883L(object):
    """
        for mini computer PocketBeagle®,
        model compass magnetometer: HMC5883L,
        protocol: i2c,
        i2c_pin_sda: 'P1_26'
        i2c_pin_scl: 'P1_28'
    """
    device_address = 0x0D
    _REG_QMC5883L_DATA_OUTPUT_X_LSB_L = 0x00
    _REG_QMC5883L_DATA_OUTPUT_X_MSB_H = 0x01
    _REG_QMC5883L_DATA_OUTPUT_Y_LSB_L = 0x02
    _REG_QMC5883L_DATA_OUTPUT_Y_MSB_H = 0x03
    _REG_QMC5883L_DATA_OUTPUT_Z_LSB_L = 0x04
    _REG_QMC5883L_DATA_OUTPUT_Z_MSB_H = 0x05
    _REG_QMC5886L_STATUS = 0x06
    _REG_QMC5883L_TEMP_OUT_H = 0x08
    _REG_QMC5883L_TEMP_OUT_L = 0x07
    _REG_QMC5883L_CONF_1 = 0x09
    _REG_QMC5883L_CONF_2 = 0x0A
    _REG_QMC5883L_SET_RESET_PERIOD = 0x0B
    _REG_QMC5883L_RESERVED = 0x0C
    _CHIP_ID = 0x0D

    _REG_DATA_UPDATE_RATE_ODR_10HZ = 0x00
    _REG_DATA_UPDATE_RATE_ODR_50HZ = 0x04
    _REG_DATA_UPDATE_RATE_ODR_100HZ = 0x08
    _REG_DATA_UPDATE_RATE_ODR_200HZ = 0x0C
    _REG_OVERSAMPLING_OSR_64 = 0xC0
    _REG_OVERSAMPLING_OSR_128 = 0x80
    _REG_OVERSAMPLING_OSR_256 = 0x40
    _REG_OVERSAMPLING_OSR_512 = 0x00
    _REG_FULL_SCALE_RNG_2G = 0x00
    _REG_FULL_SCALE_RNG_8G = 0x10

    _REG_MODE_CONTROL_STANDBY = 0x00
    _REG_MODE_CONTROL_CONTINUOUS = 0x01
    # Flags for Status Register #1.
    _REG_STAT_DRDY = 0x01  # Data Ready.
    _REG_STAT_OVL = 0x02  # Overflow flag.
    _REG_STAT_DOR = 0x04  # Data skipped for reading.

    # Flags for Status Register #2.
    _REG_INT_ENB = 0x01  # Interrupt Pin Enabling.
    _REG_POL_PNT = 0x40  # Pointer Roll-over.
    _REG_SOFT_RST = 0x80  # Soft Reset.

    _FIELD_RANGE_SENSITIVITY_2G_12000LSB_G = 12000
    _FIELD_RANGE_SENSITIVITY_8G_3000LSB_G = 3000
    _TEMPERATURE_SENSOR_SENSITIVITY = 100

    def __init__(self, i2c: int = 2):
        print('---start_init---')
        self.i2c_bus = smbus2.SMBus(i2c)  # I2C bus number used, may sometimes change on your system
        self.__check_error()
        self.mode_cont = (
                self._REG_MODE_CONTROL_CONTINUOUS |
                self._REG_DATA_UPDATE_RATE_ODR_50HZ |
                self._REG_FULL_SCALE_RNG_8G |
                self._REG_OVERSAMPLING_OSR_512
        )
        self.sensitivity_mag = self._FIELD_RANGE_SENSITIVITY_8G_3000LSB_G
        self.__write_i2c_bus_byte(self._REG_QMC5883L_CONF_2, self._REG_SOFT_RST)
        self.__write_i2c_bus_byte(self._REG_QMC5883L_CONF_2, self._REG_INT_ENB)
        self.__write_i2c_bus_byte(self._REG_QMC5883L_SET_RESET_PERIOD, 0x01)
        self.__write_i2c_bus_byte(self._REG_QMC5883L_CONF_1, self.mode_cont)

        self.__declination = 8.22
        self.__calibration = [[1.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0],
                             [0.0, 0.0, 1.0]]

    def __check_error(self):
        try:
            chip_id = self.__read_i2c_bus_byte(self._CHIP_ID)
            if chip_id != 0xff:
                print(f"Chip ID returned 0x{chip_id:x} instead of 0xff; is it the wrong chip?")
        except OSError as e:
            print(f"I2C Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def __write_i2c_bus_byte(self, registry, value):
        return self.i2c_bus.write_byte_data(self.device_address, registry, value)

    def __read_i2c_bus_byte(self, registry):
        return self.i2c_bus.read_byte_data(self.device_address, registry)

    def __read_block_data(self):
        return self.i2c_bus.read_i2c_block_data(self.device_address, self._REG_QMC5883L_DATA_OUTPUT_X_LSB_L, 8)

    def __register_shift(self, high_bit_, low_bit_):
        return c_short((high_bit_ << 8) | low_bit_).value

    def __convert_data_signet_int(self):
        """
        :return: (axix_x_signet_int, axix_y_signet_int, axix_z_signet_int, temp_signet_int)
        """
        x_l, x_h, y_l, y_h, z_l, z_h, t_l, t_h = self.__read_block_data()
        axix_x_signet_int = self.__register_shift(x_h, x_l)
        axix_y_signet_int = self.__register_shift(y_h, y_l)
        axix_z_signet_int = self.__register_shift(z_h, z_l)
        temp_signet_int = self.__register_shift(t_h, t_l)
        return (axix_x_signet_int, axix_y_signet_int, axix_z_signet_int, temp_signet_int)

    def get_temp(self) -> float:
        """
        :return: temp
        """
        temp = ((self.__convert_data_signet_int()[3]) / self._TEMPERATURE_SENSOR_SENSITIVITY)
        return temp

    def get_axix_x_y_z(self) -> Tuple:
        """
        :return: (x, y, z)
        """
        x = self.__convert_data_signet_int()[0] / self.sensitivity_mag
        y = self.__convert_data_signet_int()[1] / self.sensitivity_mag
        z = self.__convert_data_signet_int()[2] / self.sensitivity_mag
        
        return (x, y, z)

    def get_magnet(self) -> List:
        """Return the horizontal magnetic sensor vector with (x, y) calibration applied."""
        [x, y, z] = self.get_axix_x_y_z()
        if x is None or y is None:
            [x1, y1] = [x, y]
        else:
            c = self.__calibration
            x1 = x * c[0][0] + y * c[0][1] + c[0][2]
            y1 = x * c[1][0] + y * c[1][1] + c[1][2]
        return [x1, y1]

    def get_bearing_raw(self) -> float:
        """Horizontal bearing (in degrees) from magnetic value X and Y."""
        [x, y, z] = self.get_axix_x_y_z()
        if x is None or y is None:
            return None
        else:
            degrees = math.degrees(math.atan2(y, x))
            if degrees < 0:
                degrees += 360.0
            return degrees

    def get_bearing(self) -> float:
        """Horizontal bearing, adjusted by calibration and declination."""
        [x, y] = self.get_magnet()
        if x is None or y is None:
            return None
        else:
            degrees = math.degrees(math.atan2(y, x))
            if degrees < 0:
                degrees += 360.0
            degrees += self.__declination
            if degrees < 0.0:
                degrees += 360.0
            elif degrees >= 360.0:
                degrees -= 360.0
        return degrees


m = QMC5883L()
while True:
    print(m.get_temp())
    print(m.get_bearing())
    time.sleep(1)
    # TODO: write code...
