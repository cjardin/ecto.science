import RPi.GPIO as GPIO
import pigpio
import time
from servo import Servo
from flux import quad_flux

import math

import yaml

yml_configs = {}
with open('config.yml', 'r') as yml_file:
    yml_configs = yaml.safe_load(yml_file)

data = {}
median = 0.0

def calibrate( pan, tilt, flux_g):
    scan_dir_fwd = True
    deg_delay = yml_configs['servos']['deg_delay']
    step = yml_configs['servos']['scan_step']
    for i in range(0,180,step):
        pan.goto_angle(i)
        time.sleep(deg_delay)
        scan_range = []
        if scan_dir_fwd:
            scan_dir_fwd = False
            scan_range = range(0,181,step)
        else:
            scan_dir_fwd = True
            scan_range = range(180,-1,-step)

        for j in scan_range:
            tilt.goto_angle(j)
            time.sleep(deg_delay)
            if (i,j) not in data:
                data[ (i,j) ] = []
            data[ (i,j) ].append( flux_g.read()) 

def compute_biggest_delta(data):
    biggest = None
    avg_delta = 0;
    for i in range(len(data)):
        sum_delta = 0
        for j in range(len(data)):
            sum_delta += math.sqrt( pow( (data[i] - data[j]), 2) )
       
        if biggest == None or (biggest[1] < sum_delta) :
            biggest = ( i, sum_delta)
        avg_delta += sum_delta

    return biggest[0], avg_delta / len(data)


def chase(pan, tilt, flux_g):
    cur_pan_angle = 90;
    cur_tilt_angle = 90;
    while True:
        data = flux_g.read(50)

        #print(data)
        largest = compute_biggest_delta(data)

        print(largest)

        if largest[0] == yml_configs['sensors']['up']:
            cur_tilt_angle -= 1

        if largest[0] == yml_configs['sensors']['down']:
            cur_tilt_angle += 1

        if largest[0] == yml_configs['sensors']['clockwise']:
            cur_pan_angle += 1

        if largest[0] == yml_configs['sensors']['cclockwise']:
            cur_pan_angle -= 1

        if cur_pan_angle > 180:
            cur_pan_angle = 180
        elif cur_pan_angle < 0:
            cur_pan_angle = 0


        if cur_tilt_angle > 180:
            cur_tilt_angle = 180 
        elif cur_tilt_angle < 0:
            cur_tilt_angle = 0 

        pan.goto_angle(cur_pan_angle)
        tilt.goto_angle(cur_tilt_angle)


"""
  7 sensors:
  8     up : 1
  9     down : 2
 10     clockwise : 0
 11     cclockwise: 3
 12 
"""




if __name__ == '__main__':
    with  quad_flux() as flux_g:
     median = flux_g.normalize()
     time.sleep(1)
    
     with Servo( yml_configs['servos']['pan'] ) as pan:
        with Servo( yml_configs['servos']['tilt'] ) as tilt:
            #calibrate(pan,tilt,flux_g)
            chase(pan, tilt, flux_g)
            
                        
        
        
