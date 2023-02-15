import RPi.GPIO as GPIO
import pigpio
import time

class Servo:
    def __init__(self, servoPIN):
        self.servoPIN = servoPIN
        self.min_fq = 500
        self.max_fq = 2500
        self.max_rotation_deg = 180.0

    def __enter__(self):
        self.pwm = pigpio.pi('localhost', 8888)
        self.pwm.set_mode( self.servoPIN , pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(  self.servoPIN , 50 )
        self.pwm.set_servo_pulsewidth( self.servoPIN, 1500 ) ;
        return self

    def goto_angle(self, angle):
        if angle > self.max_rotation_deg or angle < 0:
            return

        target_fq = ((angle / self.max_rotation_deg) * (self.max_fq - self.min_fq)) + self.min_fq

        self.pwm.set_servo_pulsewidth( self.servoPIN, target_fq ) ;
        return

    def clean_up(self):
        self.pwm.set_PWM_dutycycle( self.servoPIN, 0 )
        self.pwm.set_PWM_frequency( self.servoPIN, 0 )
        pass
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.clean_up()


if __name__ == '__main__':
    scan_dir_fwd = True
    deg_delay = .06
    with Servo( 18 ) as pan:
        with Servo( 17 ) as tilt:
            for i in range(0,180,1):
                pan.goto_angle(i)
                time.sleep(deg_delay)
                scan_range = []
                if scan_dir_fwd:
                    scan_dir_fwd = False
                    scan_range = range(0,181,1)
                else:
                    scan_dir_fwd = True
                    scan_range = range(180,-1,-1)

                for j in scan_range:
                    tilt.goto_angle(j)
                    time.sleep(deg_delay)
        
        
