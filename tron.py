#!/usr/bin/env python3


import subprocess
import serial
import logging

# was going to use this for console logging. Moved to logging import
#import sys

#globals
variablelist = ["attract", "bank_down", "clu_lit", "clu_active", "clu_complete","discmb_active","discmb_complete","tron_active","tron_complete","gem_active","gem_complete","zuse_active","zuse_complete","lcmb_lit","lcmb_active","lcmb_complete","qmb_lit","qmb_active","qmb_complete","recog_start","recog_hit","sos_lit","sos_active","sos_complete","portal_lit"]
flags = dict.fromkeys(variablelist, False)

logger = logging.getLogger('tron_states')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')


hdlr = logging.FileHandler('/var/tmp/tron_states.log')
hdlr.setLevel(logging.DEBUG)
hdlr.setFormatter(formatter)

consoleLog = logging.StreamHandler()
consoleLog.setLevel(logging.INFO)
consoleLog.setFormatter(formatter)


logger.addHandler(hdlr) 
logger.addHandler(consoleLog)

serialport = serial.Serial("/dev/ttyUSB0", 57600, timeout=1)


while 1:
    states = serialport.readlines(None)
    logger.debug("raw states: $s" % states)
    states = list(set(states))
    logger.debug("unique states: %s" % states)
    if not states:
        # We believe this to be a new game has started but nothing to do so we should transition to recognizer and allow the states to dictate where we go from here
        if not flags['recog_start']:
            flags['recog_start'] = True
            result = subprocess.check_output(['omxd', 'X'])
            result = subprocess.check_output(['omxd', 'A', '/home/pi/media/recognizer/A-recognizer-start.mp4'])
            print("setting recognizer mode %s" % result)
    else:
        for state in states:
            state = state.rstrip()
            if 'attract_mode_on' in state:
                if not flags['attract']:
                    logger.info("Attract is running")
                    #run attract stern video
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/home/pi/media/attract/Z-Stern-Repeat.mp4'])
                    logger.debug(result)
                    logger.info("pushing Z Stern video %s" % result)
                    result = subprocess.check_output(['omxd', 'i', '/home/pi/media/attract/Z-Tron-Legacy.mp4'])
                    logger.debug(result)
                    logger.info("pushing Z Tron Video %s" % result)
                    logger.debug(result)
                    logger.info("setting attract mode %s" % result)
                    flags = dict.fromkeys(variablelist, False)
                    flags['attract'] = True
                else:
                    logger.debug("attract already running")

            elif 'null_mode_active' in state:
                print("Game Start")
                flags['attract'] = False

            elif 'recog_hit' in state:
                print("recog hit")
                if not flags['recog_hit']:
		    result = subprocess.check_output(['omxd', 'X'])
		    logger.debug(result)
		    result = subprocess.check_output(['omxd', 'I', '/home/pi/media/recognizer/B-recognizer-hit.mp4'])
		    logger.debug(result)
                    flags['recog_hit'] = True

            elif 'lcmb_lit' in state:
                print("lcmb lit")
                if not flags['lcmb_lit']:
		    result = subprocess.check_output(['omxd', 'X'])
		    logger.debug(result)
		    result = subprocess.check_output(['omxd', 'A', '/home/pi/media/lcmb/lcmb_lit.mp4'])
		    logger.debug(result)
                    flags['lcmb_lit'] = True

            elif 'lcmb_active' in state:
                print("lcmb active")
                if not flags['lcmb_active']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'I', '/home/pi/media/lcmb/lcmb_active.mp4'])
                    logger.debug(result)
                    flags['lcmb_active'] = True

            elif 'bank_down' in state:
                if not flags['bank']:
                    logger.info("bank is going down")
                    flags['bank'] = True
                    flags['recog_hit'] = False
                    result = subprocess.check_output(['omxd', 'X'])
                    result = subprocess.check_output(['omxd', 'A', '/home/pi/media/discwars/DWMB.mp4'])
             #       result = subprocess.check_output(['omxd', 'I', '/home/pi/media/recognizer/B-recognizer-hit.mp4'])
                    logger.debug("setting bank down %s" % result)
                else:
                    logger.debug("bank is already down")
            else:
                logger.info("new unhandled state %s" % state.rstrip())


