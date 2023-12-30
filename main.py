# import accelerometer_gyroscope_mpu6050
# import compass_magnetometer_qmc5883l
# import ads1115
from driver_motor_dvr8833 import DVR8833
# import driver_motor_pwm_dvr8833
from servo_sg_90 import SG90
from sonar_hy_srf05 import HY_SRF05


def main():
    # print(hex(7<<12))
    sonar = HY_SRF05()
    servo = SG90
    motor = DVR8833()
    while True:
        servo.servo_axis_x()
        servo.servo_axis_y()
        sonar_rangefinder = sonar.eyes_sonar()
        print(sonar_rangefinder)

        if sonar_rangefinder < 50:
            motor.driver_motor("stop")
        elif sonar_rangefinder > 50:
            motor.driver_motor("forward")


if __name__ == '__main__':
    main()
