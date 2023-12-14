from typing import Tuple, List
from ctypes import c_short
import smbus
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
    _FIELD_RANGE_SENSITIVITY_2G_12000LSB_G = 12000
    _FIELD_RANGE_SENSITIVITY_8G_3000LSB_G = 3000
    _TEMPERATURE_SENSOR_SENSITIVITY = 100


    def __init__(self, i2c: int = 2):
        print('---start_init---')
        self.i2c_bus = smbus.SMBus(i2c) # I2C bus number used, may sometimes change on your system
        self.i2c_bus.write_byte_data(self.device_address, self._REG_QMC5883L_CONF_1,
                                     self._REG_MODE_CONTROL_CONTINUOUS)
        self.i2c_bus.write_byte_data(self.device_address, self._REG_QMC5883L_CONF_1,
                                     self._REG_DATA_UPDATE_RATE_ODR_50HZ)
        self.i2c_bus.write_byte_data(self.device_address, self._REG_QMC5883L_CONF_1,
                                     self._REG_FULL_SCALE_RNG_8G)
        self.i2c_bus.write_byte_data(self.device_address, self._REG_QMC5883L_CONF_1,
                                     self._REG_OVERSAMPLING_OSR_256)
        time.sleep(1)
        self.sensitivity_mag = self._FIELD_RANGE_SENSITIVITY_8G_3000LSB_G
        

    def __convert_data_register_shift(self, high_bit=0, low_bit=0):
        high_bit_ = self.i2c_bus.read_byte_data(self.address_devise, high_bit)
        low_bit_ = self.i2c_bus.read_byte_data(self.address_devise, low_bit)
        signed_int_ = c_short((high_bit_ << 8) | low_bit_).value
        return signed_int_

    def get_temp(self) -> float:
        """
        :return: temp
        """
        temp_data_signed_int_ = self.__convert_data_register_shift(self._REG_QMC5883L_TEMP_OUT_H,
                                                                   self._REG_QMC5883L_TEMP_OUT_L)
        temp = ((temp_data_signed_int_) / self._TEMPERATURE_SENSOR_SENSITIVITY)
        return temp

    def get_axis_x_y_z() -> Tuple[float, float, float]:
        """
        :return: (x, y, z)
        """
        x = __convert_data_register_shift(self._REG_QMC5883L_DATA_OUTPUT_X_MSB_H, 
            self._REG_QMC5883L_DATA_OUTPUT_X_LSB_L) / self.sensitivity_mag
        y = __convert_data_register_shift(self._REG_QMC5883L_DATA_OUTPUT_Y_MSB_H, 
            self._REG_QMC5883L_DATA_OUTPUT_Y_LSB_L) / self.sensitivity_mag
        z = __convert_data_register_shift(self._REG_QMC5883L_DATA_OUTPUT_Z_MSB_H, 
            self._REG_QMC5883L_DATA_OUTPUT_Z_LSB_L) / self.sensitivity_mag
        return (x, y ,z)


