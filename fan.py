#!/usr/bin/env python

import RPi.GPIO as GPIO
import sys

def main():
    if(len(sys.argv) < 2):
        print "Usage: python fan.py [on]/[off]"
        exit()

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)

    if sys.argv[1] == 'on':
        print "Fan on"
        GPIO.output(18,GPIO.LOW)
    elif sys.argv[1] == 'off':
        print "Fan off"
        GPIO.output(18,GPIO.HIGH)
    else:
        print "Argument needs to be 'on' or 'off'"

if __name__=="__main__":
    main()