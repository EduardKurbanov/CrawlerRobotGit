from typing import Tuple
from ctypes import c_short
import Adafruit_BBIO.GPIO as GPIO
import time


class HY_SRF05(object):
    def __init__(self):
        print('---init ports hy_srf05---')
        self.eyes_sonar_trigger_gpio = 'P1_2'
        self.eyes_sonar_echo_gpio = 'P1_4'

    def eyes_sonar(self) -> float:
        """
            model sonar: 'HY-SRF05' analog 'HY-SR04',
            import Adafruit_BBIO.GPIO as GPIO,
            eyes_sonar_trigger_gpio: 'P1_2'
            eyes_sonar_echo_gpio: 'P1_4',
            :return distance: 'cm'
        """
        print('---init sonar---')
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
