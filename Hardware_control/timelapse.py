from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import time
import os
import sys
from shutil import copyfile

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

camera = PiCamera()


# Parameters for the user to modify
# Basic settings
if len(sys.argv)==5:
    folder = sys.argv[1]
    filename = sys.argv[2] 
    interval = sys.argv[3]
    steps = sys.argv[4]
else:
    print ("Required parameters: folder name, filename, interval, number of steps.")
    sys.exit()

# Minimal camera settings
camera.resolution=(960,720)
camera.ISO=400
camera.framerate = 1 # frames/sec, determines the max shutter speed
camera.shutter_speed = 200000 # exposure time in microsecs
camera.exposure_mode = 'off' #'fixedfps'
camera.awb_gains = [1,1]
camera.awb_mode = 'off'

# Advanced camera users:
# -------------------------------------------------------------
# These are other possible parameters to change, depending on experiment:
#camera.analog_gain = 1
#camera.digital_gain=1
#camera.brightness = 50
#camera.sharpness = 0
#camera.contrast = 0              # useful to take reduce the background
#camera.saturation = 0
#camera.exposure_compensation=0
#camera.image_effect='none'
#camera.color_effects=None
#camera.framerate = 0.01
#camera.exposure_speed

# Save this file with the data (to record settings etc.)
copyfile(__FILE__, os.path.join(folder, 'script.py'))

# Run the timelapse loop
    
for i in range(steps):
    
    t1 = time.time()
    print('Cycle ' + str(i))
    
    # turn the LEDs on            
    GPIO.output(29,GPIO.HIGH)

    camera.start_preview()
    sleep(1) ## preview wait time  
    fname = os.path.join(folder, filename + "_%04d.jpg"%(i))
    camera.capture(fname)
    
    #turn the LEDs off
    GPIO.output(29,GPIO.LOW)
    camera.stop_preview()

    elapsed = time.time()-t1

    # print some relevant information
    print('Elapsed cycle time: ' + str(elapsed))
    print('effective camera shutter speed :' + str(camera.shutter_speed) + '\n\n')
    # if the effective shutter speed doesn´t coincide with the one you set,
    # you must modify the camera.framerate parameter.
    
    sleep(interval-elapsed) ##  waiting time between cycles
    
GPIO.cleanup()
