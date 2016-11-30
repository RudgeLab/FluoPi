from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

camera = PiCamera()

folder = ""
filename = "exptest"
interval = 3
steps = 3

#camera settings
camera.awb_mode = 'off'
camera.awb_gain = 1
#camera.analog_gain = 1

#camera.brightness = 60
#camera.sharpness = 0
#camera.contrast = 0
#camera.saturation = 0
camera.exposure_mode = 'fixedfps'

camera.framerate = 1
camera.shutter_speed = 1000000

print camera._get_camera_settings()

for i in range(steps):

        t1 = time.time()
	sleep(interval)

        fname0 = folder + filename + "_BG_%04d.jpg"%(i)
        #camera.start_preview()
        #sleep(10)

        camera.capture(fname0)
        
	GPIO.output(29,GPIO.HIGH)
	sleep(1)
	
	#camera.start_preview()
	#sleep(10)
	
	fname = folder + filename + "_%04d.jpg"%(i)
	camera.capture(fname)

	print camera.exposure_speed
	
	GPIO.output(29,GPIO.LOW)
	#camera.stop_preview()
	
	elapsed = time.time()-t1
	print elapsed


GPIO.cleanup()

