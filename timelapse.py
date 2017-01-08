from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

camera = PiCamera()

folder = ""
filename = "exptest"
interval = 120
steps = 240

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

#camera.rotation=0
camera.ISO=0
sleep(2)
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g=camera.awb_gains
camera.awb_mode = 'off'

for i in range(steps):
    
    t1 = time.time()
            
    GPIO.output(29,GPIO.HIGH)
    #camera.start_preview()
    sleep(interval)
    camera.awb_gains = g
    
    #camera._get_camera_settings() still not sure how to use it
    fname = folder + filename + "_%04d.jpg"%(i)
    camera.capture(fname)

    GPIO.output(29,GPIO.LOW)
    #camera.stop_preview()

    elapsed = time.time()-t1
    #camera._get_camera_settings()
    print elapsed

GPIO.cleanup()
