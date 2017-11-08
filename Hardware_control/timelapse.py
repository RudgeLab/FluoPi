from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import time
import datetime
import os
import sys
from shutil import copyfile

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

camera = PiCamera()


# Parameters for the user to modify
# Basic settings
if len(sys.argv)==5:
    folder = str(sys.argv[1])            # e.g. Timelapse
    filename = str(sys.argv[2])          # e.g. im_exp1
    interval = int(sys.argv[3])     # wait time in seconds e.g. 1800
    steps = int(sys.argv[4])        # number of images   e.g 200
else:
    print ("Required parameters: folder name, filename, interval (secs), number of steps.")
    sys.exit()
    
print('folder = ' + folder + '\nfilename = ' + filename +  
      '\ninterval = ' + str(interval) + ' sec'+ '\nsteps = '+ str(steps))
 
# make the folder if it doesn't exist
if os.path.exists(folder) == False:
    os.mkdir(folder)
    
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
scriptpath = os.path.dirname(os.path.realpath(__file__))
copyfile(os.path.join(scriptpath, sys.argv[0]), os.path.join(folder, 'script.py'))

# Run the timelapse loop
    
for i in range(steps):
    
    t1 = time.time()
    print('Cycle ' + str(i))
    
    # turn the LEDs on            
    GPIO.output(29,GPIO.HIGH)

    datestr = datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    fname = os.path.join(folder, datestr + "_" + filename + "_%04d.jpg"%(i))
    camera.capture(fname)
    
    #turn the LEDs off
    GPIO.output(29,GPIO.LOW)

    elapsed = time.time()-t1

    # print some relevant information
    print('Elapsed cycle time: ' + str(elapsed))
    print('Effective camera shutter speed :' + str(camera.shutter_speed) + '\n')
    # if the effective shutter speed doesnt coincide with the one you set,
    # you must modify the camera.framerate parameter.
    
    sleep(interval-elapsed) ##  waiting time between cycles
    
GPIO.cleanup()
