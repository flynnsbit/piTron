#!/usr/bin/env python3


import subprocess
import serial
import logging
import time
import os.path


#globals

def filechecker(x,y,z):
   # x = TRUE | FALSE - Clear the playlist
   # y = Append, insert
   # z = file path

    result = ""
    if x:
        result = subprocess.check_output(['omxd', 'X'])
    if (os.path.isfile(z)):
       # file exists
        result = subprocess.check_output(['omxd', y, z])
    return result



variablelist = ["attract_mode_active", "null_mode_active", "bank_down", "discmb_restart", "discmb_return", "flynn_lit", "flynn_complete", "zen", "clu_lit", "clu_active", "clu_complete","discmb_active","discmb_complete","discmb_lit","tron_active","tron_complete","gem_active","gem_complete","zuse_active","zuse_complete","lcmb_lit","lcmb_active","lcmb_complete","qmb_lit","qmb_active","qmb_complete","recognizer_started","recog_hit","sos_lit","sos_active","sos_complete","portal_active", "portal_complete", "game_over"]
flags = dict.fromkeys(variablelist, False)

logger = logging.getLogger('tron_states')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')


hdlr = logging.FileHandler('/media/usb1/tmp/tron_states.log')
hdlr.setLevel(logging.DEBUG)
hdlr.setFormatter(formatter)

consoleLog = logging.StreamHandler()
consoleLog.setLevel(logging.DEBUG)
consoleLog.setFormatter(formatter)


logger.addHandler(hdlr) 
logger.addHandler(consoleLog)

#ROM Version checker
logger.info("getting coms version")
serialport = serial.Serial("/dev/ttyUSB0", 57600, timeout=0.5)
serialport.write("zc ver\n")
version = serialport.readlines()
ver = version.pop(1)
version = ver[4:-6]
serialport.close()
print version
logger.info("SAM COMM Version %s" % version)

if version > 31:
     logger.info("version verfied")
     result = filechecker(False, 'I', '/media/usb1/system/rom_verified.mp4')
else:
     logger.info("firmware rom needs to be updated")
     result = filechecker(False, 'I', '/media/usb1/system/error_coms.mp4')

for x in range(0, 100):  # try 100 times
    logger.info("Trying to start main code")
    try:
        serialport = serial.Serial("/dev/ttyUSB0", 57600, timeout=0.5)
        while 1:
            time.sleep(.5)
            serialport.write("zc mod 0x54A05f40\n")
            response = serialport.readlines()
            #print response            
            void = response.pop(0)
            for temp in response:
                data = temp
                ball = data[27:-20]
                players = data[16:-31]
                active_player = data[17:-30]
                #string = data[2:-4]
                state = temp
                state = state[20:-26]
                
                #print "Active Player:"
                #print active_player
                #print "Max Players:"
                #print players



                if '01' in state:
                    if not flags['attract_mode_active']:
                        logger.info("Attract is running")
                        result = filechecker(True, 'a', '/media/usb1/attract/attract.mp4')
                        logger.debug(result)
                        logger.info("setting attract mode %s" % result)
                        flags = dict.fromkeys(variablelist, False)
                        flags['attract_mode_active'] = True
                        break
                    else:
                        logger.debug("attract already running")


                elif '61' in state:
                        #Default state if bank is up
                        logger.info("Game Started - Play Enter the Grid")
                        if not flags['null_mode_active']:   
                          #  if '0' in current_player:
                          #       if not flags['player_active']:
                          #            print current_player
                          #            logger.info("Player 1")
                                      #run attract stern video
                          #            result = filechecker(True, 'I', '/media/usb1/attract/player_1.mp4')
                          #            time.sleep(5)
                          #            logger.debug(result)
                          #            logger.info("player active %s" % result)
                          #            flags = dict.fromkeys(variablelist, False)
                          #            flags['player_active'] = True
                        
                          #  else:
                          #            logger.debug("player 1 already set")
                            result = subprocess.check_output(['omxd', 'X'])
                            result = subprocess.check_output(['omxd', 'a', '/media/usb1/attract/game_start.mp4'])
                            logger.info("Enter The Grid Video Playing %s" % result)
                            flags = dict.fromkeys(variablelist, False)
                            flags['null_mode_active'] = True

                elif '67' in state:
            #Needs to be default state if bank is not down 
                        logger.info("Spinning Disc Shot - Bank Down")
                        if not flags['discmb_lit']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'a', '/media/usb1/discmb/discmb_lit.mp4'])
                            logger.info("played disc mb lit video - bank down")
                            logger.debug(result)
                            flags['discmb_lit'] = True
                            flags['discmb_active'] = False
                            flags['discmb_complete'] = False
                            flags['discmb_restart'] = False
                            flags['discmb_return'] = False
                            flags['recog_hit'] = False
           
                elif '26' in state:
                        logger.info("game over")
                        if not flags['game_over']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/attract/game_over.mp4'])
                            logger.debug(result)
                            flags['game_over'] = True
                            flags['null_mode_active'] = False
                            #flags = dict.fromkeys(variablelist, False)

                elif '5D' in state:
                        logger.info("zen")
                        if not flags['zen']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/flynn/zen.mp4'])
                            logger.debug(result)
                            flags['zen'] = True

                elif '83' in state:
                        logger.info("flynn lit")
                        if not flags['flynn_lit']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/flynn/flynn_lit.mp4'])
                            logger.debug(result)
                            flags['flynn_lit'] = True
                            flags['flynn_complete'] = False

                elif '84' in state:
                        logger.info("flynn complete")
                        if not flags['flynn_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/flynn/flynn_complete.mp4'])
                            logger.debug(result)
                            flags['flynn_complete'] = True
                            flags['flynn_lit'] = False	
							
                elif '66' in state:
                        logger.info("recog hit")
                        if not flags['recog_hit']:
 #                           result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/recognizer/recognizer_hit.mp4'])
                            logger.debug(result)
                            flags['recog_hit'] = True
                            flags['zen'] = False

                elif '49' in state:
                        logger.info("clu lit")
                        if not flags['clu_lit']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/clu/clu_lit.mp4'])
                            logger.debug(result)
                            flags['clu_lit'] = True
                            flags['clu_active'] = False
                            flags['clu_complete'] = False

                elif '40' in state:
                        logger.info("clu active")
                        if not flags['clu_active']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/clu/clu_active.mp4'])                    
                            logger.debug(result)
                            flags['clu_active'] = True

                elif '43' in state:
                        logger.info("clu complete")
                        if not flags['clu_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/clu/clu_complete.mp4'])
                            logger.debug(result)
                            flags['clu_complete'] = True
                            flags['clu_active'] = False
                            flags['clu_lit'] = False

                elif '2E' in state:
                        logger.info("discmb_active")
                        if not flags['discmb_active']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'a', '/media/usb1/discmb/discmb_active.mp4'])
                            logger.debug(result)
                            flags['discmb_complete'] = False
                            flags['discmb_lit'] = False
                            flags['discmb_active'] = True
                            flags['recog_hit'] = False

                elif '34' in state:
                        logger.info("discmb_restart")
                        if not flags['discmb_restart']:
 #                           result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/discmb/discmb_restart.mp4'])
                            logger.debug(result)
                            time.sleep(1)
                            result = subprocess.check_output(['omxd', 'L', '/media/usb1/attract/game_start.mp4'])
                            logger.debug(result)
                            flags['discmb_restart'] = True
                            flags['discmb_lit'] = False
                            flags['discmb_active'] = False
                            flags['discmb_return'] = False
                           

                elif '36' in state:
                        logger.info("discmb_return")
                        if not flags['discmb_return']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'a', '/media/usb1/discmb/discmb_active.mp4'])
                            logger.debug(result)
                            flags['discmb_return'] = True

                elif '33' in state:
                        logger.info("discmb_complete")
                        if not flags['discmb_complete']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/discmb/discmb_complete.mp4'])
                            logger.debug(result)
                            time.sleep(1)
                            result = subprocess.check_output(['omxd', 'L', '/media/usb1/attract/game_start.mp4'])                            
                            logger.debug(result)
                            flags['discmb_complete'] = True
                            flags['discmb_active'] = False
                            flags['discmb_lit'] = False
                            flags['discmb_restart'] = False
                            flags['discmb_return'] = False


                elif '65' in state:
                        logger.info("tron_active")
                        if not flags['tron_active']:
                           # result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
 #TRON DISABLED FOR NOW     result = subprocess.check_output(['omxd', 'I', '/media/usb1/tron/tron_active.mp4'])
                            logger.debug(result)
                            flags['tron_active'] = True
                            flags['tron_complete'] = False

                elif '64' in state:
                        logger.info("tron_complete")
                        if not flags['tron_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
#TRON DISABLED FOR NOW      result = subprocess.check_output(['omxd', 'I', '/media/usb1/tron/tron_complete.mp4'])
#Could add multiple if not flags so that this doesn't fire when active modes are running
                            logger.debug(result)
                            flags['tron_complete'] = True
                            flags['tron_active'] = False

                elif '45' in state:
                        logger.info("gem_active")
                        if not flags['gem_active']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'a', '/media/usb1/gem/gem_active.mp4'])
                            #result = subprocess.check_output(['omxd', 'a', '/media/usb1/gem/gem_active.mp4'])
                            logger.debug(result)
                            flags['gem_active'] = True
                            flags['gem_compelte'] = False

                elif '48' in state:
                        logger.info("gem_complete")
                        if not flags['gem_complete']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/gem/gem_complete.mp4'])
                            logger.debug(result)                            
                            time.sleep(1)
                            result = subprocess.check_output(['omxd', 'L', '/media/usb1/attract/game_start.mp4'])
                            logger.debug(result)
                            flags['gem_complete'] = True
                            flags['gem_active'] = False

                elif '57' in state:
                        logger.info("zuse_active")
                        if not flags['zuse_active']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/zuse/zuse_active.mp4'])
                            logger.debug(result)
                            flags['zuse_active'] = True
                            flags['zuse_complete'] = False

                elif '5C' in state:
                        logger.info("zuse_complete")
                        if not flags['zuse_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/zuse/zuse_complete.mp4'])
                            logger.debug(result)
                            flags['zuse_complete'] = True
                            flags['zuse_active'] = False

                elif '4D' in state:
                        logger.info("lcmb_lit")
                        if not flags['lcmb_lit']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/lcmb/lcmb_lit.mp4'])
                            logger.debug(result)
                            flags['lcmb_lit'] = True
                            flags['lcmb_active'] = False
                            flags['lcmb_compelte'] = False

                elif '4E' in state:
                        logger.info("lcmb_active")
                        if not flags['lcmb_active']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'a', '/media/usb1/lcmb/lcmb_active.mp4'])
                            logger.debug(result)
                            flags['lcmb_active'] = True

                elif '53' in state:
                        logger.info("lcmb_complete")
                        if not flags['lcmb_complete']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/lcmb/lcmb_complete.mp4'])
                            logger.debug(result)
                            time.sleep(1)
                            result = subprocess.check_output(['omxd', 'L', '/media/usb1/attract/game_start.mp4'])
                            logger.debug(result)
                            flags['lcmb_complete'] = True
                            flags['lcmb_lit'] = False
                            flags['lcmb_active'] = False

                elif '38' in state:
                        logger.info("qmb_lit")
                        if not flags['qmb_lit']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/qmb/qmb_lit.mp4'])
                            logger.debug(result)
                            flags['qmb_lit'] = True
                            flags['qmb_active'] = False
                            flags['qmb_complete'] = False

                elif '39' in state:
                        logger.info("qmb_active")
                        if not flags['qmb_active']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'a', '/media/usb1/qmb/qmb_active.mp4'])
                            #result = subprocess.check_output(['omxd', 'a', '/media/usb1/qmb/qmb_active.mp4'])
                            logger.debug(result)
                            flags['qmb_active'] = True

                elif '3F' in state:
                        logger.info("qmb_complete")
                        if not flags['qmb_complete']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/qmb/qmb_complete.mp4'])
                            logger.debug(result)
                            time.sleep(1)
                            result = subprocess.check_output(['omxd', 'L', '/media/usb1/attract/game_start.mp4'])
                            logger.debug(result)
                            flags['qmb_complete'] = True
                            flags['qmb_lit'] = False
                            flags['qmb_active'] = False

                elif '6C' in state:
                        logger.info("sos_lit")
                        if not flags['sos_lit']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/sos/sos_lit.mp4'])
                            logger.debug(result)
                            flags['sos_lit'] = True
                            flags['sos_active'] = False
                            flags['sos_complete'] = False

                elif '6B' in state:
                        logger.info("sos_active")
                        if not flags['sos_active']:
                            #result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/sos/sos_active.mp4'])
                            #result = subprocess.check_output(['omxd', 'a', '/media/usb1/sos/sos_active.mp4'])
                            logger.debug(result)
                            flags['sos_active'] = True

                elif '78' in state:
                        logger.info("sos_complete")
                        if not flags['sos_complete']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/sos/sos_complete.mp4'])
                            logger.debug(result)
                            time.sleep(1)
                            result = subprocess.check_output(['omxd', 'L', '/media/usb1/attract/game_start.mp4'])
                            logger.debug(result)
                            flags['sos_complete'] = True
                            flags['sos_lit'] = False
                            flags['sos_active'] = False

                elif '87' in state:
                        logger.info("portal_active")
                        if not flags['portal_active']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'a', '/media/usb1/portal/portal_active.mp4'])
                            logger.debug(result)
                            flags['portal_active'] = True

                elif '8C' in state:
                        logger.info("portal_complete")
                        if not flags['portal_complete']:
                            result = subprocess.check_output(['omxd', 'X'])
                            logger.debug(result)
                            result = subprocess.check_output(['omxd', 'I', '/media/usb1/portal/portal_complete.mp4'])
                            logger.debug(result)
                            time.sleep(1)
                            result = subprocess.check_output(['omxd', 'L', '/media/usb1/attract/game_start.mp4'])
                            logger.debug(result)
                            flags['portal_active'] = False
                            flags['portal_complete'] = True

                elif '00' in state:
                    logger.info("No Active States")
                        #if not flags['bank_down']:
                            #logger.info("bank is going down")
                            #flags['bank_down'] = True
                            #flags['recog_hit'] = False
                       #     result = subprocess.check_output(['omxd', 'X'])
                        #    result = subprocess.check_output(['omxd', 'A', '/media/usb1/discmb/discmb_lit.mp4'])
                     #       result = subprocess.check_output(['omxd', 'I', '/media/usb1/recognizer/B-recognizer-hit.mp4'])
                            #logger.debug("setting bank down %s" % result)
                        #else:
                            #logger.debug("bank is already down")
                elif '19' in state:
                    logger.info("Ball Ended")
                else:
                    logger.info("new unhandled state %s" % state.rstrip())

    except serial.SerialException as str_error:
        serialport.close()
        strError = str(str_error)
        logger.info ("Error communicating with Serial Interface")
        logger.error("%s" % strError.rstrip())
        result = filechecker(False, 'I', '/media/usb1/system/serial_failure.mp4')
        time.sleep(10)  # wait for 2 seconds before trying to fetch the data again
        pass
