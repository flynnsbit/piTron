#!/usr/bin/env python3


import subprocess
import serial
import logging

# was going to use this for console logging. Moved to logging import
#import sys

#globals

variablelist = ["attract_mode_active", "null_mode_active", "bank_down", "clu_lit", "clu_active", "clu_complete","disc_war_active","discmb_complete","disc_mb_active","tron_active","tron_complete","gem_active","gem_complete","zuse_active","zuse_complete","lcmb_lit","lcmb_active","lcmb_complete","qmb_lit","qmb_active","qmb_complete","recognizer_started","recog_hit","sos_lit","sos_active","sos_complete","portal_lit"]
flags = dict.fromkeys(variablelist, False)

logger = logging.getLogger('tron_states')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')


hdlr = logging.FileHandler('/media/usb1/tron_states_tls.log')
hdlr.setLevel(logging.DEBUG)
hdlr.setFormatter(formatter)

consoleLog = logging.StreamHandler()
consoleLog.setLevel(logging.DEBUG)
consoleLog.setFormatter(formatter)


logger.addHandler(hdlr) 
logger.addHandler(consoleLog)

serialport = serial.Serial("/dev/ttyUSB0", 57600, timeout=0.5)
#result = subprocess.call(['dd', 'if=/dev/zero', 'of=/dev/fb0'])

while 1:
#    result = subprocess.call(['dd', 'if=/dev/zero', 'of=/dev/fb0'])
    states = serialport.readlines(None)
    logger.debug("raw states: $s" % states)
    states = list(set(states))
    logger.debug("unique states: %s" % states)
 #   if not states:
  #      if not flags['recog_start']:
   #         flags['recog_start'] = True
           # result = subprocess.check_output(['omxd', 'X'])
           # result = subprocess.check_output(['omxd', 'A', '/media/usb1/recognizer/A-recognizer-start.mp4'])
           # print("setting recognizer mode %s" % result)
   # else:
    for state in states:
            state = state.rstrip()
            if 'attract_mode_active' in state:
                if not flags['attract_mode_active']:
                    logger.info("Attract is running")
                    #run attract stern video
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    #result = subprocess.check_output(['omxd', 'A', '/media/usb1/attract/Z-Stern-Repeat.mp4'])
                    result = subprocess.check_output(['omxd', 'a', '/media/usb1/attract/attract.mp4'])
                    logger.debug(result)
                    logger.info("setting attract mode %s" % result)
                    flags = dict.fromkeys(variablelist, False)
                    flags['attract_mode_active'] = True
                    break
                else:
                    logger.debug("attract already running")

            elif 'null_mode_active' in state:
                print("Game Start- Null Mode Active")
                if not flags['null_mode_active']:                
                    result = subprocess.check_output(['omxd', 'X'])
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/attract/game_start.mp4'])
                    print("Enter The Grid Video Playing %s" % result)
                    flags = dict.fromkeys(variablelist, False)
                    flags['null_mode_active'] = True
   
            elif 'recognizer_started' in state:
                print("recognizer started")
                if not flags['recognizer_started']:
		    result = subprocess.check_output(['omxd', 'X'])
		    logger.debug(result)
		    result = subprocess.check_output(['omxd', 'A', '/media/usb1/recognizer/recognizer_hit.mp4'])
		    logger.debug(result)
                    flags['recognizer_started'] = True

            elif 'lcmb_lit' in state:
                print("lcmb lit")
                if not flags['lcmb_lit']:
		    result = subprocess.check_output(['omxd', 'X'])
		    logger.debug(result)
		    result = subprocess.check_output(['omxd', 'A', '/media/usb1/lcmb/lcmb_lit.mp4'])
		    logger.debug(result)
                    flags['lcmb_lit'] = True

            elif 'lcmb_active' in state:
                print("lcmb active")
                if not flags['lcmb_active']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/lcmb/lcmb_active.mp4'])
                    logger.debug(result)
                    flags['lcmb_active'] = True

            elif 'clu_lit' in state:
                print("Clu Lit")
                if not flags['clu_lit']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/clu/clu_lit.mp4'])
                    logger.debug(result)
                    flags['clu_lit'] = True

            elif 'clu_active' in state:
                print("clu active")
                if not flags['clu_active']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/clu/clu_active.mp4'])
                    logger.debug(result)
                    flags['clu_active'] = True

            elif 'clu_complete' in state:
                print("clu complete")
                if not flags['clu_complete']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/clu/clu_complete.mp4'])
                    logger.debug(result)
                    flags['clu_complete'] = True

            elif 'disc_war_active' in state:
                print("disc_war_active")
                if not flags['disc_war_active']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/discmb/discmb_lit.mp4'])
                    print("played disc mb active video")
                    logger.debug(result)
                    flags['disc_war_active'] = True

            elif 'disc_mb_active' in state:
                print("disc_mb_active")
                if not flags['disc_mb_active']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/discmb/discmb_active.mp4'])
                    logger.debug(result)
                    flags['disc_mb_active'] = True

            elif 'discmb_complete' in state:
                print("discmb_complete")
                if not flags['discmb_complete']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/discmb/discmb_complete.mp4'])
                    logger.debug(result)
                    flags['discmb_complete'] = True

            elif 'tron_active' in state:
                print("tron_active")
                if not flags['tron_active']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'I', '/media/usb1/tron/tron_active.mp4'])
                    logger.debug(result)
                    flags['tron_active'] = True

            elif 'tron_complete' in state:
                print("tron_complete")
                if not flags['tron_complete']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/tron/tron_complete.mp4'])
                    logger.debug(result)
                    flags['tron_complete'] = True

            elif 'gem_active' in state:
                print("gem_active")
                if not flags['gem_active']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/gem/gem_active.mp4'])
                    logger.debug(result)
                    flags['gem_active'] = True

            elif 'gem_complete' in state:
                print("gem_complete")
                if not flags['gem_complete']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/gem/gem_complete.mp4'])
                    logger.debug(result)
                    flags['gem_complete'] = True

            elif 'zuse_active' in state:
                print("zuse_active")
                if not flags['zuse_active']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/zuse/zuse_active.mp4'])
                    logger.debug(result)
                    flags['zuse_active'] = True

            elif 'zuse_complete' in state:
                print("zuse_complete")
                if not flags['zuse_complete']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/zuse/zuse_complete.mp4'])
                    logger.debug(result)
                    flags['zuse_complete'] = True

            elif 'lcmb_lit' in state:
                print("lcmb_lit")
                if not flags['lcmb_lit']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/lcmb/lcmb_lit.mp4'])
                    logger.debug(result)
                    flags['lcmb_lit'] = True

            elif 'lcmb_active' in state:
                print("lcmb_active")
                if not flags['lcmb_active']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/lcmb/lcmb_active.mp4'])
                    logger.debug(result)
                    flags['lcmb_active'] = True

            elif 'lcmb_complete' in state:
                print("lcmb_complete")
                if not flags['lcmb_complete']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/lcmb/lcmb_complete.mp4'])
                    logger.debug(result)
                    flags['lcmb_complete'] = True

            elif 'qmb_lit' in state:
                print("qmb_lit")
                if not flags['qmb_lit']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/qmb/qmb_lit.mp4'])
                    logger.debug(result)
                    flags['qmb_lit'] = True

            elif 'qmb_active' in state:
                print("qmb_active")
                if not flags['qmb_active']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/qmb/qmb_active.mp4'])
                    logger.debug(result)
                    flags['qmb_active'] = True

            elif 'qmb_complete' in state:
                print("qmb_complete")
                if not flags['qmb_complete']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/qmb/qmb_complete.mp4'])
                    logger.debug(result)
                    flags['qmb_complete'] = True

            elif 'sos_lit' in state:
                print("sos_lit")
                if not flags['sos_lit']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/sos/sos_lit.mp4'])
                    logger.debug(result)
                    flags['sos_lit'] = True

            elif 'sos_active' in state:
                print("sos_active")
                if not flags['sos_active']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/sos/sos_active.mp4'])
                    logger.debug(result)
                    flags['sos_active'] = True

            elif 'sos_complete' in state:
                print("sos_complete")
                if not flags['sos_complete']:
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/sos/sos_complete.mp4'])
                    logger.debug(result)
                    flags['sos_complete'] = True

            elif 'bank_down' in state:
                if not flags['bank_down']:
                    logger.info("bank is going down")
                    result = subprocess.check_output(['omxd', 'X'])
                    logger.debug(result)
                    result = subprocess.check_output(['omxd', 'A', '/media/usb1/discmb/discmb_lit.mp4'])
                    print("played disc mb active video")
                    logger.debug(result)
                    flags['bank_down'] = True
                    #flags['recog_hit'] = False
               #     result = subprocess.check_output(['omxd', 'X'])
                #    result = subprocess.check_output(['omxd', 'A', '/media/usb1/discmb/discmb_lit.mp4'])
             #       result = subprocess.check_output(['omxd', 'I', '/media/usb1/recognizer/B-recognizer-hit.mp4'])
                    logger.debug("setting bank down %s" % result)
                else:
                    logger.debug("bank is already down")
            else:
                logger.info("new unhandled state %s" % state.rstrip())


