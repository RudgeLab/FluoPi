from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

camera = PiCamera()

folder = ""
filename = "valdivia_test_%04d.jpg"
interval = 300
steps = 24

camera.ISO=0
sleep(2)
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = [1,1]

for i in range(steps):
    
    t1 = time.time()
            
    GPIO.output(29,GPIO.HIGH)
    #camera.start_preview()
    sleep(interval)
    
    #camera._get_camera_settings() still not sure how to use it

    fname = os.path.join(folder, filename%(i))
    #folder + filename + "_%04d.jpg"%(i)
    camera.capture(fname)

    GPIO.output(29,GPIO.LOW)
    #camera.stop_preview()

    elapsed = time.time()-t1
    #camera._get_camera_settings()
    print elapsed

GPIO.cleanup()
