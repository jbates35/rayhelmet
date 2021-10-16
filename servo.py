import time
import threading
import pigpio

class servo:

    OPEN_SERVO = 2
    CLOSE_SERVO = 1
    NOACTION = False
    SERVO_AVAIL = True
    SERVO_BUSY = False

    def __init__(self, pi, gpio, servo_close, servo_open):
        self.openval = servo_open
        self.closeval = servo_close
        self.pi = pi
        self.gpio = gpio
        self.servo_val_real = self.closeval
        self.servo_val = self.closeval
        self.servo_state = servo.SERVO_BUSY
        self.servo_command = servo.CLOSE_SERVO
        self.pi.set_mode(self.gpio, pigpio.OUTPUT)
        self.update_pin = threading.Thread(target=self.update_pin)
        self.update_pin.start()
        self.update_val = threading.Thread(target=self.update_val)
        self.update_val.start()

    # Run script for servo
    def update_pin(self):
        while True:
            val = (self.servo_val_real * 2000/180) + 500
            self.pi.set_servo_pulsewidth(self.gpio, val)

    def update_val(self):
        while True:
            if self.servo_state == servo.SERVO_BUSY:
                self.servo_val_real = self.servo_val
                self.servo_state = servo.SERVO_AVAIL

    def open(self):
        self.servo_command = servo.OPEN_SERVO
        self.servo_state = servo.SERVO_BUSY
        self.servo_val = self.openval

    def close(self):
        self.servo_command = servo.CLOSE_SERVO
        self.servo_state = servo.SERVO_BUSY
        self.servo_val = self.closeval
