#!/usr/bin/python

import time
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

co_adc = 0

last_read = 0
torerance = 5

while True:
	print readadc(co_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	time.sleep(.3)
