#to run: python turnON.py GPIO_number
#where GPIO_number have to be an integer. e.g. 29

import RPi.GPIO as GPIO
import sys

# Set the GPIO number where LEDs control is conected
if len(sys.argv)==2:
    GPIO_num = str(sys.argv[1])            # e.g. Timelapse

else:
    GPIO_num = 29   #GPIO 29 is used as the default

GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_num, GPIO.OUT)

GPIO.output(GPIO_num,GPIO.HIGH)
