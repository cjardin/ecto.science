from servo import Servo
import time

if __name__ == '__main__':
    with Servo( 18 ) as pan:
        with Servo( 17 ) as tilt:

            time.sleep(2)

            pan.goto_angle(0)
            tilt.goto_angle(0)
            time.sleep(2)

            pan.goto_angle(90)
            tilt.goto_angle(90)
            time.sleep(2)
        

            pan.goto_angle(180)
            tilt.goto_angle(180)
            time.sleep(2)
        
