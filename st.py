#!/usr/bin/env python3

import serial
serialport = serial.Serial("/dev/ttyUSB0", 57600, timeout=0.5)

attract = 0
bank = 0
clu = 0
disc = 0
gem = 0
lcmb = 0
qmb = 0
recog = 0
sos = 0
tron = 0
zuse = 0
#game = True


while 1:

        state = serialport.readlines()

        for data in state:
                if 'attract_mode_on' in data:
			print data
                        print "Attract is 1"
                        #run attract stern video
			attract = 1
                        game = False

		if 'recog_hit' in data:
			print data			
			print "Recog Hit"
			#run advance recognizer animation 
			recog = 1
		if 'bank_down' in data:
			print data
			print "Bank down"
			#run Sam picked up ny recognizer video
			bank = 1 
		else:
			print data

#elif 'recog_hit' in data:
#                       print "Recognizer hit"

#elif 'bank_down' in data:
#                       print "Bank down"


