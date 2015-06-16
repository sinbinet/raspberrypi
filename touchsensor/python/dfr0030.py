#!/usr/bin/python

import RPi.GPIO as GPIO
import time

def reading(sensor):

    TOUCH = 17
    LED = 16

    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TOUCH, GPIO.IN)
    
    while True:
		if GPIO.input(TOUCH):
			print "push"
		else:
			print "0"
		time.sleep(.3)
        
try:
	reading(0)
except KeyboardInterrupt:
	print "Quit"
	GPIO.cleanup()
