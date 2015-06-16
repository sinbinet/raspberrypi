# Editor : Jeong, Pil Mhan
# Author : Kowonsik, github.com/kowonsik
# Author : Jeonghoonkang, github.com/jeonghoonkang

## This code for T100, ELT CO2 sensor

import serial,os,time
import sys
import RPi.GPIO as GPIO

import json
import requests
import fcntl, socket, struct

from co2led import *

DEBUG_PRINT = 1
SERIAL_READ_BYTE = 12
FILEMAXBYTE = 1024 * 1024 * 100 #100MB

CO2LED_BLUE_PIN = 17
CO2LED_GREEN_PIN = 22
CO2LED_RED_PIN = 27


def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' %ord(char) for char in info[18:24]])

macAddr = getHwAddr('eth0')
macAddr = macAddr.replace(':','.')

level = 0
ppm = 0

def checkAlignment(incoming):
    idxNum = incoming.find('m')
    # idxNum is 9, correct
    offset = idxNum - 9 
    if offset > 0 :
        new_str = incoming[offset:]
        new_str = new_str + incoming[:offset]
    if offset < 0 :
        offset = 12 + offset 
        new_str = incoming[offset:]
        new_str = new_str + incoming[:offset]
    return new_str
    
def init_process():
    print " "
    print "MSG - now starting to read SERIAL PORT"
    print " "
    ledall_off()

if __name__== "__main__" :
    # call raspi init...
    init_process()

    # open RASPI serial device, 38400
    try: 
        serial_in_device = serial.Serial('/dev/ttyAMA0',38400)
    except serial.SerialException, e:
        ledall_off()

    while True:
        ppm = 0
        try:
            in_byte = serial_in_device.read(SERIAL_READ_BYTE) 
            pos = 0
        except serial.SerialException, e:
            ledall_off()
        if not (len(in_byte) is SERIAL_READ_BYTE) : 
            print 'serial byte read count error'
            continue
        # sometimes, 12 byte alighn is in-correct
        # espacially run on /etc/rc.local
        if not in_byte[9] is 'm':
            shift_byte = checkAlignment(in_byte)
            in_byte = shift_byte
        if ('ppm' in in_byte):
            if DEBUG_PRINT :
                print '-----\/---------\/------ DEBUG_PRINT set -----\/---------\/------ '
                for byte in in_byte :
                    print "serial_in_byte[%d]: " %pos,
                    pos += 1
                    if ord(byte) is 0x0d :
                        print "escape:", '0x0d'," Hex: ", byte.encode('hex')
                        continue
                    elif ord(byte) is 0x0a :
                        print "escape:", '0x0a'," Hex: ", byte.encode('hex')
                        continue
                    print " String:", byte,  "    Hex: ", byte.encode('hex')
            if not (in_byte[2] is ' ') :
                ppm += (int(in_byte[2])) * 1000
            if not (in_byte[3] is ' ') :
                ppm += (int(in_byte[3])) * 100
            if not (in_byte[4] is ' ') :
                ppm += (int(in_byte[4])) * 10
            if not (in_byte[5] is ' ') :
                ppm += (int(in_byte[5]))  

            logline = ' CO2 Level is '+ str(ppm) + ' ppm' 
            ledall_off()

            if DEBUG_PRINT :
                print logline

            if ppm > 2100 : 
                # cancel insert data into DB, skip.... since PPM is too high,
                # it's abnormal in indoor buidling
                ledred_on()
                ### maybe change to BLINK RED, later
                continue
            else :
				pass

        # level = 1, 0~800 ppm,     blue- LED
        # level = 2, 800~1000 ppm,  blue green - LED
        # level = 3, 1000~1300 ppm, green - LED
        # level = 4, 1300~1600 ppm, white - LED
        # level = 5, 1600~1900 ppm, yellow - LED
        # level = 6, 1900~ 2100 ppm,     purple - LED, if over 2100 - red LED

        if ppm < 800 :  
            ledblue_on()
        elif ppm < 1000 :  
            ledbluegreen_on()
        elif ppm < 1300 :  
            ledgreen_on()
        elif ppm < 1600:  
            ledwhite_on()
        elif ppm < 1900:  
            ledyellow_on()
        elif ppm >= 1900 :  
            ledpurple_on()
      
