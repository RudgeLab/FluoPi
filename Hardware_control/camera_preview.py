#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Reference: http://picamera.readthedocs.io/en/release-1.10/index.html

from picamera import PiCamera
from time import sleep
from datetime import timedelta
import datetime

# Basic procedure as in point 3.5 Capturing consistent images  from readthedocs.io

# 1 Create Camera instance 
camera = PiCamera()
# The Pi’s camera has three ports, the still port (for images), the video port (recording), and the preview port.
# Their output is independet so 

# 2 Set resolution
camera.resolution=(960,720) 	# Retrieves or sets the resolution at which image captures, video recordings, and previews will be captured.

# 3 Set frame rate
camera.framerate = 1 # frames/sec, determines the max shutter speed

# 4 Set ISO to the desired value
camera.iso = 500    # Retrieves or sets the apparent ISO setting of the camera.

# 5 Fix the ss
camera.shutter_speed = 300000 #e

# 6 Wait for the automatic gain control to settle (Analog and Digital Gain)
sleep(5)

# Notice: we will skip step 7 as we need the automatic analog and digital gains for live previewing
# as capture and preview use different ports disabling Auto gains now will give a correct captured image but a
# probably dark preview. Uncomment if you are just capturing and not previewing

# 7 Turn off automatic gain (fix AG and DG) 
#camera.exposure_mode = 'off'

# 8 Disable AWB gain control
camera.awb_mode = 'off'

# 9 Now fix the Red & Blue gains
camera.awb_gains = [1.0,1.0]


# Advanced camera users:
# -------------------------------------------------------------
# These are other possible parameters to change, depending on experiment:

#camera.analog_gain       			# Retrieves the current analog gain of the camera.
#camera.awb_gains = [1,1] 			# Gets or sets the auto-white-balance gains of the camera. [red, blue]. This attribute only has an effect when awb_mode is set to 'off'.
#camera.awb_mode = 'off'    		        # Retrieves or sets the auto-white-balance mode of the camera.
#camera.brightness = 50				# Retrieves or sets the brightness setting of the camera. [0,100]
#camera.color_effects=None			# Retrieves or sets the current color effect applied by the camera.
#camera.contrast = 0        		        # Retrieves or sets the contrast setting of the camera. Useful to take reduce the background
#camera.digital_gain				# Retrieves the current digital gain of the camera.
#camera.exposure_compensation=0  	        # Retrieves or sets the exposure compensation level of the camera.
#camera.exposure_mode = 'off'	 	        # Retrieves or sets the exposure mode of the camera.
#camera.exposure_speed				# Retrieves the current shutter speed of the camera.
#camera.framerate = 0.01			# Retrieves or sets the framerate at which video-port based image captures, video recordings, and previews will run.
#camera.image_denoise				# Retrieves or sets whether denoise will be applied to image captures. Default true
#camera.image_effect='none'
#camera.image_effect_params
#camera.meter_mode
#camera.rotation = 90  				# Retrieves or sets the current rotation of the camera’s image.
#camera.saturation = 0  			# Retrieves or sets the saturation setting of the camera. 
#camera.sensor_mode				# Retrieves or sets the input mode of the camera’s sensor. setting this property does nothing unless the camera has been initialized with a sensor mode other than 0.
#camera.sharpness = 0 				# Retrieves or sets the sharpness setting of the camera. [-100, 100]
#camera.shutter_speed = 500000 		        # Retrieves or sets the shutter speed of the camera in microseconds.
    
# alpha window transparency 
#alpha =0
#camera.start_preview(alpha =200)
# -------------------------------------------------------------


# 10 Start preview
camera.start_preview()

# Wait for "Intro" input 
raw_input('Wait for the preview window, then press enter to take photo and close preview: ')

# 7 Turn off automatic gain (fix AG and DG) 
camera.exposure_mode = 'off'

# 11 Take Picture
# Any attempt to capture an image without using the video port optiob will (temporarily)
# select the 2592x1944 mode while the capture is performed (this is what causes
# the flicker you sometimes see when a preview is running while a still image is captured).
datestr = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
fname = "preview_" + datestr + ".png"
camera.capture(fname, 'png')  # use_video_port defaults to False which means that the camera’s image port is used. This port is slow but produces better quality pictures.

# Query shutter speed value
e = camera.exposure_speed
print('Shutter Speed: ' + str(e))

# Query AWB gains
g = camera.awb_gains
print('AWB gains ' + str(g))

# Query iso
i = camera.iso
print('ISO ' + str(i))

# Query A gain
a=camera.analog_gain
print('A Gain ' + str(a))

# Query D gains
d=camera.digital_gain
print('D Gain ' + str(d))

b=camera.brightness
print('brightness ' + str(b))

c=camera.contrast
print('contrast ' + str(c))

camera.stop_preview()

camera.close()
