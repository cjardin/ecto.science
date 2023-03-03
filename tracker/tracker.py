import RPi.GPIO as GPIO
import pigpio
import time
from servo import Servo
from flux import quad_flux


data = {}
median = 0.0

if __name__ == '__main__':
    scan_dir_fwd = True
    deg_delay = .06
    with  quad_flux() as flux_g:
     median = flux_g.normalize()
     time.sleep(1)
    
     with Servo( 0 ) as pan:
        with Servo( 1 ) as tilt:
            for i in range(0,180,10):
                pan.goto_angle(i)
                scan_range = []
                if scan_dir_fwd:
                    scan_dir_fwd = False
                    scan_range = range(0,181,10)
                else:
                    scan_dir_fwd = True
                    scan_range = range(180,-1,-10)

                for j in scan_range:
                    tilt.goto_angle(j)
            
                    if (i,j) not in data:
                        data[ (i,j) ] = []
                    data[ (i,j) ].append( flux_g.read() ) 

                        
        
        
