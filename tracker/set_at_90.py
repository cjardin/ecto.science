from servo import Servo
import time

if __name__ == '__main__':
    with Servo( 18 ) as pan:
        with Servo( 17 ) as tilt:

            time.sleep(2)

        
