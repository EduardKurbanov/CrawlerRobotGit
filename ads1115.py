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

    _REG_ADS1115_CONFIG_OS_SINGLE = 0x8000

    _REG_ADS1115_CONFIG_MUX_AINP_AIN0_and_AINN_AIN1 = 0x0000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN0_and_AINN_AIN3 = 0x1000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN1_and_AINN_AIN3 = 0x2000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN2_and_AINN_AIN3 = 0x3000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN0_and_AINN_GND = 0x4000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN1_and_AINN_GND = 0x5000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN2_and_AINN_GND = 0x6000
    _REG_ADS1115_CONFIG_MUX_AINP_AIN3_and_AINN_GND = 0x7000

    _REG_ADS1115_CONFIG_PGA_FSR__6_144V = 0x0000
    _REG_ADS1115_CONFIG_PGA_FSR__4_096V = 0x0200
    _REG_ADS1115_CONFIG_PGA_FSR__2_048V = 0x0400
    _REG_ADS1115_CONFIG_PGA_FSR__1_024V = 0x0600
    _REG_ADS1115_CONFIG_PGA_FSR__0_512V = 0x0800
    _REG_ADS1115_CONFIG_PGA_FSR__0_256V = 0x0A00

    _REG_ADS1115_CONFIG_MODE_SINGLE = 0x100

    _REG_ADS1115_CONFIG_DR_8_SPS = 0x0000
    _REG_ADS1115_CONFIG_DR_16_SPS = 0x0020
    _REG_ADS1115_CONFIG_DR_32_SPS = 0x0040
    _REG_ADS1115_CONFIG_DR_64_SPS = 0x0060
    _REG_ADS1115_CONFIG_DR_128_SPS = 0x0080
    _REG_ADS1115_CONFIG_DR_250_SPS = 0x00A0
    _REG_ADS1115_CONFIG_DR_475_SPS = 0x00C0
    _REG_ADS1115_CONFIG_DR_860_SPS = 0x00E0

    _REG_ADS1115_COMP_MODE_TRAD = 0x00
    _REG_ADS1115_COMP_MODE_WINDOWS = 0x10

    _REG_ADS1115_COMP_POL_ACTIVE_LOW = 0x00
    _REG_ADS1115_COMP_POL_ACTIVE_HIGH = 0x08

    _REG_ADS1115_COMP_NON_LAT = 0x0000
    _REG_ADS1115_COMP_LAT = 0x0004

    _REG_ADS1115_COMP_QUE_AFTER_1_CONVER = 0x0000
    _REG_ADS1115_COMP_QUE_AFTER_2_CONVER = 0x0001
    _REG_ADS1115_COMP_QUE_AFTER_3_CONVER = 0x0002
    _REG_ADS1115_COMP_QUE_DISABLE_CONVER = 0x0003

    pga_ads1115 = {
        6144: _REG_ADS1115_CONFIG_PGA_FSR__6_144V,
        4096: _REG_ADS1115_CONFIG_PGA_FSR__4_096V,
        2048: _REG_ADS1115_CONFIG_PGA_FSR__2_048V,
        1024: _REG_ADS1115_CONFIG_PGA_FSR__1_024V,
        512: _REG_ADS1115_CONFIG_PGA_FSR__0_512V,
        256: _REG_ADS1115_CONFIG_PGA_FSR__0_256V
    }

    sps_ads1115 = {
        8: _REG_ADS1115_CONFIG_DR_8_SPS,
        16: _REG_ADS1115_CONFIG_DR_16_SPS,
        32: _REG_ADS1115_CONFIG_DR_32_SPS,
        64: _REG_ADS1115_CONFIG_DR_64_SPS,
        128: _REG_ADS1115_CONFIG_DR_128_SPS,
        250: _REG_ADS1115_CONFIG_DR_250_SPS,
        475: _REG_ADS1115_CONFIG_DR_475_SPS,
        860: _REG_ADS1115_CONFIG_DR_860_SPS
    }

    channel_adc_ads1115 = {
        0: _REG_ADS1115_CONFIG_MUX_AINP_AIN0_and_AINN_GND,
        1: _REG_ADS1115_CONFIG_MUX_AINP_AIN1_and_AINN_GND,
        2: _REG_ADS1115_CONFIG_MUX_AINP_AIN2_and_AINN_GND,
        3: _REG_ADS1115_CONFIG_MUX_AINP_AIN3_and_AINN_GND
    }

    def __init__(self, i2c: int = 2):
        print('---start_init---')
        try:
            self.i2c_bus = smbus2.SMBus(i2c)
        except:
            raise IOError("Could not find i2c device")

    def __mode_cont(self, channel_adc: int = 0, pga_adc: int = 6144, sps_adc: int = 250):

        if channel_adc not in self.channel_adc_ads1115:
            raise ValueError("Wrong channel, use channel 0-3")

        if pga_adc not in self.pga_ads1115:
            raise ValueError("Wrong pga, use pga 6144, 4096, 2048, 1024, 512, 256")

        if sps_adc not in self.sps_ads1115:
            raise ValueError("Wrong sps, use sps 8, 16, 32, 64, 128, 250, 475, 860")

        mode_cont = (
                self._REG_ADS1115_CONFIG_OS_SINGLE |
                self.channel_adc_ads1115[channel_adc] |
                self.pga_ads1115[pga_adc] |
                self._REG_ADS1115_CONFIG_MODE_SINGLE |
                self.sps_ads1115[sps_adc] |
                self._REG_ADS1115_COMP_QUE_DISABLE_CONVER |
                self._REG_ADS1115_COMP_NON_LAT |
                self._REG_ADS1115_COMP_POL_ACTIVE_LOW |
                self._REG_ADS1115_COMP_MODE_TRAD
        )

        bytes = [(mode_cont >> 8) & 0xFF, mode_cont & 0xFF]
        return bytes

    def __write_i2c_bus_byte(self, registry, value):
        return self.i2c_bus.write_i2c_block_data(self.device_address, registry, value)

    def __read_i2c_bus_byte(self, registry, value):
        return self.i2c_bus.read_i2c_block_data(self.device_address, registry, value)

    def get_read_adc(self, channel_adc: int = 0, pga_adc: int = 6144, sps_adc: int = 250) -> float:
        self.__write_i2c_bus_byte(self._REG_ADS1115_ADDRESS_POINTER_CONFIG,
                                  self.__mode_cont(channel_adc, pga_adc, sps_adc))
        delay = 1.0 / sps_adc + 0.0001
        time.sleep(delay)
        data_adc = self.__read_i2c_bus_byte(self._REG_ADS1115_POINTER_CONVERSION, 2)
        val = (data_adc[0] << 8) | (data_adc[1])
        if val > 0x7FFF:
            return (val - 0xFFFF) * pga_adc / 32768.0
        else:
            return ((data_adc[0] << 8) | (data_adc[1])) * pga_adc / 32768.0


s = ADS1115()
while True:
    print(s.get_read_adc(0))
    time.sleep(0.1)
