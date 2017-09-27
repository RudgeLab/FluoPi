from picamera import PiCamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

GPIO.output(29,GPIO.LOW)

GPIO.cleanup()
