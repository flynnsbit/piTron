#!/usr/bin/env python3


import subprocess
import serial
import logging
import time
import os.path
# was going to use this for console logging. Moved to logging import
#import sys

#globals

def filechecker(x,y,z):
   # x = TRUE | FALSE - Clear the playlist
   # y = Append, insert
   # z = file path
   #basically here we are going to do some sanity checking if the file exists and if it does then we call the omx$
    result = ""
    if x:
        result = subprocess.check_output(['omxd', 'X'])
    if (os.path.isfile(z)):
       # file exists so lets do the needful
        result = subprocess.check_output(['omxd', y, z])
    return result



variablelist = ["attract", "null_mode_active", "bank_down", "clu_lit", "clu_active", "clu_complete","disc_war_active","discmb_complete","disc_mb_active","tron_active","tron_complete","gem_active","gem_complete","zuse_active","zuse_complete","lcmb_lit","lcmb_active","lcmb_complete","qmb_lit","qmb_active","qmb_complete","recog_start","recog_hit","sos_lit","sos_active","sos_complete","portal_lit","game_over","ball_over","zen"]
flags = dict.fromkeys(variablelist, False)

logger = logging.getLogger('tron_states')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')


hdlr = logging.FileHandler('/var/tmp/tron_states.log')
hdlr.setLevel(logging.DEBUG)
hdlr.setFormatter(formatter)

consoleLog = logging.StreamHandler()
consoleLog.setLevel(logging.DEBUG)
consoleLog.setFormatter(formatter)


logger.addHandler(hdlr) 
logger.addHandler(consoleLog)



for x in range(0, 100):  # try 100 times
    print "Trying to start"
    try:
        # msg.send()
        # put your logic here
        serialport = serial.Serial("/dev/ttyUSB0", 57600, timeout=0.5)
        while 1:
            time.sleep(1)
            serialport.write("zc mod 0x54A05f40\n")
            response = serialport.readlines()
            print response
            void = response.pop(0)
            for temp in response:
                data = temp
                ball = data[27:-20]
                players = data[16:-31]
                current_player = data [17:-30]
                #string = data[2:-4]
                state = temp
                state = state[20:-26]
                print state
                if '01' in state:
                    if not flags['attract']:
                        logger.info("Attract is running")
                        #run attract stern video
                        result = filechecker(True, 'a', '/home/pi/media/attract/Z-Tron-Legacy.mp4')
                        logger.debug(result)
                        logger.info("setting attract mode %s" % result)
                        flags = dict.fromkeys(variablelist, False)
                        flags['attract'] = True
                        break
                    else:
                        logger.debug("attract already running")

                elif '61' in state:
            #Default state if bank is up
                        print("Game Start- Recognizer Animation")
                        if not flags['null_mode_active']:                
                            result = subprocess.check_output(['omxd', 'X'])
                            result = subprocess.check_output(['omxd', 'A', '/home/pi/media/attract/game_start.mp4'])
                            print("Enter The Grid Video Playing %s" % result)
                            flags = dict.fromkeys(variablelist, False)
                            flags['null_mode_active'] = True

                elif '67' in state:
            #Needs to be default state if bank is not down 
                        print("Spinning Disc Shot - Bank Down")
                        if not flags['disc_war_active']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/discmb/discmb_lit.mp4'])
                            print("played disc mb active video")
                            logger.debug(result)
                            flags['disc_war_active'] = True
           
                elif '26' in state:
                        print("ball over")
                        if not flags['ball_over']:
                          #  result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/attract/ball-over.mp4'])
                            logger.debug(result)
                            flags['ball_over'] = True

                elif '5D' in state:
                        print("zen")
                        if not flags['zen']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/flynn/zen.mp4'])
                            logger.debug(result)
                            flags['zen'] = True

                elif '66' in state:
                        print("recog hit")
                        if not flags['recog_hit']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/recognizer/A-recognizer-start.mp4'])
                            logger.debug(result)
                            flags['recog_hit'] = True

                elif '4D' in state:
                        print("lcmb lit")
                        if not flags['lcmb_lit']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/lcmb/lcmb_lit.mp4'])
                            logger.debug(result)
                            flags['lcmb_lit'] = True

                elif '4E' in state:
                        print("lcmb active")
                        if not flags['lcmb_active']:
                        #    result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/lcmb/lcmb_active.mp4'])
                            result = subprocess.check_output(['omxd', 'a', '/home/pi/media/lcmb/lcmb_active.mp4'])
                            logger.debug(result)
                            flags['lcmb_active'] = True

                elif '49' in state:
                        print("Clu Lit")
                        if not flags['clu_lit']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/clu/clu_lit.mp4'])
                            logger.debug(result)
                            flags['clu_lit'] = True

                elif '40' in state:
                        print("clu active")
                        if not flags['clu_active']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/clu/clu_active.mp4'])                    
                            result = subprocess.check_output(['omxd', 'a', '/home/pi/media/clu/clu_active.mp4'])
                            logger.debug(result)
                            flags['clu_active'] = True

                elif '43' in state:
                        print("clu complete")
                        if not flags['clu_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/clu/clu_complete.mp4'])
                            logger.debug(result)
                            flags['clu_complete'] = True

                elif '2E' in state:
                        print("disc_mb_active")
                        if not flags['disc_mb_active']:
                         #   result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'A', '/home/pi/media/discmb/discmb_active.mp4'])
                            logger.debug(result)
                            flags['disc_mb_active'] = True

                elif '33' in state:
                        print("discmb_complete")
                        if not flags['discmb_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/discmb/discmb_complete.mp4'])
                            logger.debug(result)
                            flags['discmb_complete'] = True
                            flags['null_mode_active'] = False

                elif '65' in state:
                        print("tron_active")
                        if not flags['tron_active']:
                           # result = subprocess.check_output(['omxd', 'X'])
                           # logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/tron/tron_active.mp4'])
                            logger.debug(result)
                            flags['tron_active'] = True

                elif '64' in state:
                        print("tron_complete")
                        if not flags['tron_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/tron/tron_complete.mp4'])
                            logger.debug(result)
                            flags['tron_complete'] = True

                elif '45' in state:
                        print("gem_active")
                        if not flags['gem_active']:
                          #  result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/gem/gem_active.mp4'])
                            result = subprocess.check_output(['omxd', 'a', '/home/pi/media/gem/gem_active.mp4'])
                            logger.debug(result)
                            flags['gem_active'] = True

                elif '48' in state:
                        print("gem_complete")
                        if not flags['gem_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/gem/gem_complete.mp4'])
                            logger.debug(result)
                            flags['gem_complete'] = True

                elif '57' in state:
                        print("zuse_active")
                        if not flags['zuse_active']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/zuse/zuse_active.mp4'])
                            result = subprocess.check_output(['omxd', 'a', '/home/pi/media/zuse/zuse_active.mp4'])
                            logger.debug(result)
                            flags['zuse_active'] = True

                elif '5C' in state:
                        print("zuse_complete")
                        if not flags['zuse_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/zuse/zuse_complete.mp4'])
                            logger.debug(result)
                            flags['zuse_complete'] = True

                elif '4D' in state:
                        print("lcmb_lit")
                        if not flags['lcmb_lit']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/lcmb/lcmb_lit.mp4'])
                            logger.debug(result)
                            flags['lcmb_lit'] = True

                elif '4E' in state:
                        print("lcmb_active")
                        if not flags['lcmb_active']:
                           # result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/lcmb/lcmb_active.mp4'])
                            result = subprocess.check_output(['omxd', 'a', '/home/pi/media/lcmb/lcmb_active.mp4'])
                            logger.debug(result)
                            flags['lcmb_active'] = True

                elif '53' in state:
                        print("lcmb_complete")
                        if not flags['lcmb_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/lcmb/lcmb_complete.mp4'])
                            logger.debug(result)
                            flags['lcmb_complete'] = True

                elif '38' in state:
                        print("qmb_lit")
                        if not flags['qmb_lit']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/qmb/qmb_lit.mp4'])
                            logger.debug(result)
                            flags['qmb_lit'] = True

                elif '39' in state:
                        print("qmb_active")
                        if not flags['qmb_active']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/qmb/qmb_active.mp4'])
                            result = subprocess.check_output(['omxd', 'a', '/home/pi/media/qmb/qmb_active.mp4'])
                            logger.debug(result)
                            flags['qmb_active'] = True

                elif '3F' in state:
                        print("qmb_complete")
                        if not flags['qmb_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/qmb/qmb_complete.mp4'])
                            logger.debug(result)
                            flags['qmb_complete'] = True

                elif '6C' in state:
                        print("sos_lit")
                        if not flags['sos_lit']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/sos/sos_lit.mp4'])
                            logger.debug(result)
                            flags['sos_lit'] = True

                elif '6B' in state:
                        print("sos_active")
                        if not flags['sos_active']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/sos/sos_active.mp4'])
                            result = subprocess.check_output(['omxd', 'a', '/home/pi/media/sos/sos_active.mp4'])
                            logger.debug(result)
                            flags['sos_active'] = True

                elif '78' in state:
                        print("sos_complete")
                        if not flags['sos_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/home/pi/media/sos/sos_complete.mp4'])
                            logger.debug(result)
                            flags['sos_complete'] = True

                elif '00' in state:
                    print("00 State")
                        #if not flags['bank_down']:
                            #logger.info("bank is going down")
                            #flags['bank_down'] = True
                            #flags['recog_hit'] = False
                       #     result = subprocess.check_output(['omxd', 'X'])
                        #    result = subprocess.check_output(['omxd', 'A', '/home/pi/media/discmb/discmb_lit.mp4'])
                     #       result = subprocess.check_output(['omxd', 'I', '/home/pi/media/recognizer/B-recognizer-hit.mp4'])
                            #logger.debug("setting bank down %s" % result)
                        #else:
                            #logger.debug("bank is already down")
                else:
                    logger.info("new unhandled state %s" % state.rstrip())

    except serial.SerialException as str_error:
        serialport.close()
        strError = str(str_error)
        print "Error communicating with Serial Interface"
        logger.error("%s" % strError.rstrip())
        result = filechecker(True, 'I', '/home/pi/media/error/error_coms.mp4')
        time.sleep(10)  # wait for 2 seconds before trying to fetch the data again
        pass
