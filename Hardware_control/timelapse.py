import os
import sys
import time
import datetime

from RPi import GPIO
from shutil import copyfile
from picamera import PiCamera

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

camera = PiCamera()

# Parameters for the user to modify
# Basic settings
if len(sys.argv) == 5:
    folder = str(sys.argv[1])   # e.g. Timelapse
    filename = str(sys.argv[2]) # e.g. im_exp1
    interval = int(sys.argv[3]) # wait time in seconds e.g. 1800
    steps = int(sys.argv[4])    # number of images e.g 200
else:
    print("Required parameters: folder name, filename, interval (secs), number of steps.")
    sys.exit()
    
print(f'folder = {folder}')
print(f'filename = {filename}')
print(f'interval = {interval} sec')
print(f'steps = {steps}')
 
# make the folder if it doesn't exist
if not os.path.exists(folder):
    os.mkdir(folder)
    
# Minimal camera settings
camera.resolution = (960,720)
camera.ISO = 400
camera.framerate = 1 # frames/sec, determines the max shutter speed
camera.shutter_speed = 200000 # exposure time in microsecs
camera.exposure_mode = 'off' #'fixedfps'
camera.awb_gains = [1,1]
camera.awb_mode = 'off'

# Advanced camera users:
# -------------------------------------------------------------
# These are other possible parameters to change, depending on experiment:
#camera.analog_gain = 1
#camera.digital_gain = 1
#camera.brightness = 50
#camera.sharpness = 0
#camera.contrast = 0              # useful to take reduce the background
#camera.saturation = 0
#camera.exposure_compensation = 0
#camera.image_effect = 'none'
#camera.color_effects = None
#camera.framerate = 0.01
#camera.exposure_speed

# Save this file with the data (to record settings etc.)
scriptpath = os.path.dirname(os.path.realpath(__file__))
copyfile(os.path.join(scriptpath, sys.argv[0]), os.path.join(folder, 'script.py'))

# Run the timelapse loop
    
for i in range(steps):
    
    t1 = time.time()
    print(f'Cycle {i}')
    
    # turn the LEDs on            
    GPIO.output(29,GPIO.HIGH)

    datestr = datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    fname = os.path.join(folder, f'{datestr}_{filename}_{i:04}.jpg')
    camera.capture(fname)
    
    # turn the LEDs off
    GPIO.output(29,GPIO.LOW)

    elapsed = time.time() - t1

    # print some relevant information
    print(f'Elapsed cycle time: {elapsed}')
    print(f'Effective camera shutter speed: {camera.shutter_speed} \n')
    # if the effective shutter speed doesnt coincide with the one you set,
    # you must modify the camera.framerate parameter.
    
    time.sleep(interval-elapsed) ##  waiting time between cycles
    
GPIO.cleanup()
