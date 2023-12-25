from typing import Tuple, List
from ctypes import c_short
import smbus2
import time


class ADS1115(object):
    """
      for mini computer PocketBeagle®,
      model adc: ADS1115,
      protocol: i2c,
      i2c_pin_sda: 'P1_26'
      i2c_pin_scl: 'P1_28'
    """
    device_address = 0x48
    _REG_ADS1115_POINTER_CONVERSION = 0x00
    _REG_ADS1115_ADDRESS_POINTER_CONFIG = 0x01
    _REG_ADS1115_POINTER_LOW_THRESHOLD = 0x02
    _REG_ADS1115_POINTER_HIGH_THRESHOLD = 0x03
    _REG_ADS1115_CONFIG_OS_SINGLE = 8000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN0_and_AINN_AIN1 = 0x00
    _REG_ADS1115_CONFIG_MUX_AINP_AIN0_and_AINN_AIN3 = 0x1000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN1_and_AINN_AIN3 = 0x2000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN2_and_AINN_AIN3 = 0x3000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN0_and_AINN_GND = 0x4000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN1_and_AINN_GND = 0x5000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN2_and_AINN_GND = 0x6000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN3_and_AINN_GND = 0x7000
    _REG_ADS1115_CONFIG_PGA_FSR__6_144V = 0x00
    _REG_ADS1115_CONFIG_PGA_FSR__4_096V = 0x200
    _REG_ADS1115_CONFIG_PGA_FSR__2_048V = 0x400
    _REG_ADS1115_CONFIG_PGA_FSR__1_024V = 0x600
    _REG_ADS1115_CONFIG_PGA_FSR__0_512V = 0x800
    _REG_ADS1115_CONFIG_PGA_FSR__0_256V = 0xA00
    _REG_ADS1115_CONFIG_MODE_SINGLE = 0x100
    _REG_ADS1115_CONFIG_DR_8_SPS = 0x00
    _REG_ADS1115_CONFIG_DR_16_SPS = 0x20
    _REG_ADS1115_CONFIG_DR_32_SPS = 0x40
    _REG_ADS1115_CONFIG_DR_64_SPS = 0x60
    _REG_ADS1115_CONFIG_DR_128_SPS = 0x80
    _REG_ADS1115_CONFIG_DR_250_SPS = 0xA0
    _REG_ADS1115_CONFIG_DR_475_SPS = 0xC0
    _REG_ADS1115_CONFIG_DR_860_SPS = 0xE0
    _REG_ADS1115_COMP_MODE_WINDOWS = 0x10
    _REG_ADS1115_COMP_POL_ACTIVE_HIGH = 0x08
    _REG_ADS1115_COMP_LAT = 0x04
    _REG_ADS1115_COMP_QUE_AFTER_1_CONVER = 0x00
    _REG_ADS1115_COMP_QUE_AFTER_2_CONVER = 0x02
    _REG_ADS1115_COMP_QUE_AFTER_3_CONVER = 0x04
    _REG_ADS1115_COMP_QUE_DISABLE_CONVER = 0x06

    def __init__(self, i2c: int = 2):
        print('---start_init---')
        self.i2c_bus = smbus2.SMBus(i2c)

    def __mode_cont(self, channel_adc=0):
        channel_values = {
            0: self._REG_ADS1115_CONFIG_MUX_AINP_AIN0_and_AINN_GND,
            1: self._REG_ADS1115_CONFIG_MUX_AINP_AIN1_and_AINN_GND,
            2: self._REG_ADS1115_CONFIG_MUX_AINP_AIN2_and_AINN_GND,
            3: self._REG_ADS1115_CONFIG_MUX_AINP_AIN3_and_AINN_GND,
        }
        if channel_adc not in channel_values:
            raise ValueError("Wrong channel, use channel 0-3")

        mode_cont = (
                self._REG_ADS1115_CONFIG_OS_SINGLE |
                channel_values[channel_adc] |
                self._REG_ADS1115_CONFIG_PGA_FSR__6_144V |
                self._REG_ADS1115_CONFIG_MODE_SINGLE |
                self._REG_ADS1115_CONFIG_DR_128_SPS
        )
        return mode_cont

    def __write_i2c_bus_byte(self, registry, value):
        return self.i2c_bus.write_byte_data(self.device_address, registry, value)

    def __read_i2c_bus_byte(self, registry):
        return self.i2c_bus.read_word_data(self.device_address, registry)

    def get_read_adc(self, channel_adc):
        self.__write_i2c_bus_byte(self._REG_ADS1115_ADDRESS_POINTER_CONFIG, self.__mode_cont(channel_adc))
        time.sleep(0.1)
        data_adc = self.__read_i2c_bus_byte(self._REG_ADS1115_POINTER_CONVERSION)
        swapped_data = ((data_adc << 8) & 0xFF00) | ((data_adc >> 8) & 0xFF)
        return swapped_data
