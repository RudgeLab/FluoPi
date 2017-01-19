from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import time
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

camera = PiCamera()

folder = "Valdivia_13_1_17"
filename = "image"
interval = 300
steps = 420

#camera settings

#camera.analog_gain = 1
#camera.digital_gain=1
#camera.brightness = 50
#camera.sharpness = 0
#camera.contrast = 0
#camera.saturation = 0
#camera.exposure_compensation=0
#camera.image_effect='none'
#camera.color_effects=None

camera.resolution=(960,720)
camera.ISO=400
sleep(2)
camera.framerate = 1 # frames/sec, determines the max shutter speed
camera.shutter_speed = 200000 # exposure time in microsecs
##camera.framerate = 0.01
##camera.exposure_speed

## preview allows camera to settle on sensible auto gain values
##camera.start_preview()
##sleep(3)
##camera.stop_preview()

camera.exposure_mode = 'off' #'fixedfps'
camera.awb_gains = [1,1]
camera.awb_mode = 'off'



print camera.shutter_speed

for i in range(steps):
    
    t1 = time.time()
            
    GPIO.output(29,GPIO.HIGH)

    camera.start_preview()
    sleep(1) ## preview wait time  
    camera.awb_gains = [1,1]
    #camera._get_camera_settings() still not sure how to use it
    fname = os.path.join(folder, filename + "_%04d.jpg"%(i))
    camera.capture(fname)

    GPIO.output(29,GPIO.LOW)
    camera.stop_preview()

    elapsed = time.time()-t1

    #camera._get_camera_settings()
    print elapsed
    print camera.shutter_speed
    sleep(interval-elapsed) ##  loop wait time
    
GPIO.cleanup()
