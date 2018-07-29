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
    interval = int(sys.argv[3])     	 # wait time in seconds e.g. 1800
    steps = int(sys.argv[4])        	 # number of images   e.g 200
else:
    print ("Required parameters: folder name, filename, interval (secs), number of steps.")
    sys.exit()
    
print('folder = ' + folder + '\nfilename = ' + filename +  
      '\ninterval = ' + str(interval) + ' sec'+ '\nsteps = '+ str(steps))
 
# make the folder if it doesn't exist
if os.path.exists(folder) == False:
    os.mkdir(folder)

#Variables
#hRes = 960
#vRes = 720
fr = 1
iso = 500
ss= 300000
redG = 1.0
blueG = 1.0
b= 50
c= 0 

# Basic procedure as in point 3.5 Capturing consistent images  from readthedocs.io

# 1 Create Camera instance 
camera = PiCamera()
# The Pi’s camera has three ports, the still port (for images), the video port (recording), and the preview port.
# Their output is independet so 

# 2 Set resolution
camera.resolution=(960,720) 	# Retrieves or sets the resolution at which image captures, video recordings, and previews will be captured.

# 3 Set frame rate
camera.framerate = fr # frames/sec, determines the max shutter speed

# 4 Set ISO to the desired value
camera.iso = iso    # Retrieves or sets the apparent ISO setting of the camera.

# 5 Fix the ss
camera.shutter_speed = ss #e

# 6 Wait for the automatic gain control to settle (Analog and Digital Gain)
sleep(5)

# Notice: we will skip step 7 as we need the automatic analog and digital gains for live previewing
# as capture and preview use different ports disabling Auto gains now will give a correct captured image but a
# probably dark preview. Uncomment if you are just capturing and not previewing

# 7 Turn off automatic gain (fix AG and DG) 
# camera.exposure_mode = 'off'

# 8 Disable AWB gain control
camera.awb_mode = 'off'

# 9 Now fix the Red & Blue gains
camera.awb_gains = [redG,blueG]


# Advanced camera users:
# -------------------------------------------------------------
# These are other possible parameters to change, depending on experiment:

#camera.analog_gain       			# Retrieves the current analog gain of the camera.
#camera.awb_gains = [1,1] 			# Gets or sets the auto-white-balance gains of the camera. [red, blue]. This attribute only has an effect when awb_mode is set to 'off'.
#camera.awb_mode = 'off'    		# Retrieves or sets the auto-white-balance mode of the camera.
#camera.brightness = 50				# Retrieves or sets the brightness setting of the camera. [0,100], Default 50
#camera.color_effects=None			# Retrieves or sets the current color effect applied by the camera.
#camera.contrast = 0        		# Retrieves or sets the contrast setting of the camera. Useful to take reduce the background [0,100]. Default 0 
#camera.digital_gain				# Retrieves the current digital gain of the camera.
#camera.exposure_compensation=0  	# Retrieves or sets the exposure compensation level of the camera.
#camera.exposure_mode = 'off'	 	# Retrieves or sets the exposure mode of the camera.
#camera.exposure_speed				# Retrieves the current shutter speed of the camera.
#camera.framerate = 0.01			# Retrieves or sets the framerate at which video-port based image captures, video recordings, and previews will run.
#camera.image_denoise				# Retrieves or sets whether denoise will be applied to image captures. Default true
#camera.image_effect='none'
#camera.image_effect_params
#camera.meter_mode
#camera.rotation = 90  				# Retrieves or sets the current rotation of the camera’s image.
#camera.saturation = 0  			# Retrieves or sets the saturation setting of the camera. 
#camera.sensor_mode					# Retrieves or sets the input mode of the camera’s sensor. setting this property does nothing unless the camera has been initialized with a sensor mode other than 0.
#camera.sharpness = 0 				# Retrieves or sets the sharpness setting of the camera. [-100, 100]
#camera.shutter_speed = 500000 		# Retrieves or sets the shutter speed of the camera in microseconds.
    
# alpha window transparency 
# alpha =0
# camera.start_preview(alpha =200)
# -------------------------------------------------------------

# 10 Start preview
camera.start_preview()

# Wait for "Intro" input 
raw_input('Wait for the preview window, then press enter to take photo and close preview: ')

# 7 Turn off automatic gain (fix AG and DG) 
camera.exposure_mode = 'off'

#12 Stop preview
camera.stop_preview() 

# -------------------------------------------------------------
	
	
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
    fname = os.path.join(folder, datestr + "_" + filename + "_%04d.png"%(i))
    camera.capture(fname,'png')
    
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
