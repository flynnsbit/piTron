#!/usr/bin/env python3

import serial
import time
serialport = serial.Serial("/dev/ttyUSB0", 57600, timeout=0.5)
while 1:
	time.sleep(1)
	serialport.write("zc mod 0x54A05f40\n")
	response = serialport.readlines()
	void = response.pop(0)
	for temp in response:
        	data = temp
		data = data[20:-26]
		print data
