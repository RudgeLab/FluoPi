from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

camera = PiCamera()

folder = "/mnt/usb/TL30_10/"
filename = "timlap"
interval = 600
steps = 288

#camera settings
camera.awb_mode = 'fluorescent'
#camera.brightness = 60
#camera.sharpness = 0
#camera.contrast = 0
#camera.saturation = 0
#camera.exposure_mode = 0

for i in range(steps):

        fname0 = folder + filename + "_BG3_%04d.jpg"%(i)
        camera.start_preview()
	sleep(10)
        camera.capture(fname0)
        
	GPIO.output(29,GPIO.HIGH)
	sleep(1)
	
	camera.start_preview()
	sleep(10)
	
	fname = folder + filename + "_3_%04d.jpg"%(i)
	camera.capture(fname)
	
	GPIO.output(29,GPIO.LOW)
	camera.stop_preview()
	sleep(interval-21)


GPIO.cleanup()

