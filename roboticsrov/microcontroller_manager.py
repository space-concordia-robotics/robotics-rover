#!/usr/bin/env python2.7

import serial


ser = serial.Serial(0)  # Opens first serial port

print ser.name          
ser.write("hello")
ser.close()
