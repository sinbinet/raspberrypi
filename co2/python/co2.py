#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import serial

try:
	port = serial.Serial("/dev/ttyAMA0", baudrate=38400, timeout=None)
	print "%s open" % port

	while True:
		try:
			print "count"
			data = port.read()
			time.sleep(.1)
			tmp_bytes = port.inWaiting()
			data += port.read(tmp_bytes)
			print data
		except Exception, e:
			print str(e)

except KeyboardInterrupt:
	print "Quit"
	GPIO.cleanup()
