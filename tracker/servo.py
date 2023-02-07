import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, servoPIN):
        self.servoPIN = servoPIN
        self.min_ds = 5.0
        self.max_ds = 10.0
        self.max_rotation_deg = 180.0

    def __enter__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servoPIN, GPIO.OUT)
        self.pin = GPIO.PWM(self.servoPIN, 50)
        self.pin.start(2.5)
        return self

    def goto_angle(self, angle, stable=True):

        print(angle)
    
        if angle > self.max_rotation_deg or angle < 0:
            return

        target_ds = ((angle / self.max_rotation_deg) * (self.max_ds - self.min_ds)) + self.min_ds

        print(target_ds)
        self.pin.ChangeDutyCycle(target_ds)
        if stable : 
            time.sleep(.2)
            self.pin.ChangeDutyCycle(0)
        return

    def clean_up(self):
        self.pin.stop()
        GPIO.cleanup()
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.clean_up()


if __name__ == '__main__':
    with Servo( 18 ) as pan:
        with Servo( 17 ) as tilt:
            for i in range(0,180,10):
                pan.goto_angle(i)
                time.sleep(1)
                for j in range(0,180,10):
                    tilt.goto_angle(j)
                    time.sleep(1)
        
        
