#!/usr/bin/env python

import time, os
#import wiringpi2
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	if (adcnum > 7) or (adcnum < 0):
		return -1
	GPIO.output(cspin, True)

	GPIO.output(clockpin, False)
	GPIO.output(cspin, False)

	commandout = adcnum
	commandout |= 0x18
	commandout <<= 3
	for i in range(5):
		if commandout & 0x80:
			GPIO.output(mosipin, True)
		else:
			GPIO.output(mosipin, False)
		commandout <<= 1
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)

	adcout = 0

	for i in range(12):
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)
		adcout <<= 1
		if GPIO.input(misopin):
			adcout |= 0x1

	GPIO.output(cspin, True)

	adcout >>= 1
	return adcout

SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

dust_adc = 0
ILED = 4

GPIO.setup(4, GPIO.OUT)
GPIO.output(4, False)

while True:
	GPIO.output(4, True)
	#time.sleep(0.0001)
	#GPIO.output(4, False)

	time.sleep(0.00028)
	print readadc(dust_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	time.sleep(0.00004)
	GPIO.output(4, False)
	time.sleep(.3)
	'''
    GPIO.output(4, True) # on 
    time.sleep(0.000175) # 0.000280
    r = readadc(dust_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
    time.sleep(0.000000) # 0.000040
    # set low GPIO 5
    GPIO.output(4, False) # off 
    time.sleep(0.009550)  # 0.00968

    if r > 187 :
        um = (500.0/2.9)*(3.3/1024)*r-103.44
    else :
        um = 0.1
    if r > 10 :
        print "r :",r
	time.sleep(3)
	'''
