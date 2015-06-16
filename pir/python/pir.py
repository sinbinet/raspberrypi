#!/usr/bin/python

import time
import RPi.GPIO as GPIO

def reading(sensor):

    PIR = 18

    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    
    if sensor == 0:
        GPIO.setup(PIR, GPIO.IN)
	return GPIO.input(PIR)
        
        GPIO.cleanup()
    else:
        print "Incorrect function varible."

        
try:
	while True:
		print reading(0)
		time.sleep(1)
except KeyboardInterrupt:
	print "Quit"
	GPIO.cleanup()


