class ADS1115(object):
    """
      for mini computer PocketBeagle®,
      model adc: ADS1115,
      protocol: i2c,
      i2c_pin_sda: 'P1_26'
      i2c_pin_scl: 'P1_28'
    """

    def __init__(self, i2c: int = 2):
        print('---start_init---')
        self.i2c_bus = smbus.SMBus(i2c)
