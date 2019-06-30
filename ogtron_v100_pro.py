#!/usr/bin/env python3
#v100_debug
#Changes - Adding all code for scoring, overlay, ball, player and pygame into main code

import subprocess
import serial
import logging
import time
import os.path
import os
import pygame

os.putenv('SDL_NOMOUSE', '1')
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')

pygame.init()

#no need to re-make these again each loop.
font = pygame.font.Font("ethnocen.ttf",80)
font2 = pygame.font.Font("ethnocen.ttf",30)

fps = 30
clock = pygame.time.Clock()
X = 1920
Y = 1080
screen = pygame.display.set_mode((X, Y ))

#reference the base overlay that will be used between the video and the overlays for scoring, player, etc.
baseOverlay = pygame.image.load('background_1920_final.png').convert()

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

#trying to build logic for a 4 player game, how do you handle dict for each flags without having 4 sets if if then statements looping
modelist = ["default_state", "default_state_run", "ball_end", "ball_end_player", "attract_mode_active", "null_mode_active", "bank_down", "discmb_restart", "discmb_return", "flynn_lit", "flynn_complete", "zen", "clu_lit", "clu_active", "clu_complete","discmb_active","discmb_complete","discmb_lit","tron_active","tron_complete","gem_active","gem_complete","zuse_active","zuse_complete","lcmb_lit","lcmb_active","lcmb_complete","qmb_lit","qmb_active","qmb_complete","recognizer_started","recog_hit","sos_lit","sos_active","sos_complete","portal_active", "portal_complete", "game_over"]
golden_flags = dict.fromkeys(modelist, False)

#here we store the state ID to the flag map so we can reset a default state at ball loss
default_state_map = {
'61': 'null_mode_active',
'67': 'discmb_lit',
'66': 'recog_hit'
}

#global
flagInitialization = True
playerFlags=list()

#logging states
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
try:
     logger.info("getting coms version")
     serialport = serial.Serial("/dev/ttyUSB0", 57600, timeout=0.5)
     serialport.write("zc ver\n")
     version = serialport.readlines()
     ver = version.pop(1)
     version = ver[4:-6]
     serialport.close()
     print version
     logger.info("pitron_v100 - SAM COMM Version %s" % version)

except serial.SerialException as str_error:
        serialport.close()
        strError = str(str_error)
        logger.info ("Error communicating with Serial Interface")
        logger.error("%s" % strError.rstrip())
        #Add code for pygame font to blit the error to the screen instead of video
        result = filechecker(False, 'I', '/media/usb1/system/serial_failure.mp4')
        time.sleep(10)  # wait for 10 seconds before trying to fetch the data again
        pass

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
            serialport.write("zc mod 0x54A05f40\n") #Get game states
            response1 = serialport.readlines()
            serialport.write("zc mod 0x5c073564 0\n") #Get Scoring
            response2 = serialport.readlines()
            void = response2.pop(0)
            #pop the responses and check for no data and prevent script fail
            gameData = [response1.pop(0) for __ in xrange(len(response1))]
            scoreData = [response2.pop(0) for __ in xrange(len(response2))]
            if len(gamedata) > 0
            #print response
            void = gameData.pop(0)
            screen.blit(baseOverlay,(0,0))
            for temp in gameData:
             #print temp
             srecord = temp[:2]
             if "S3" in srecord:         #crc checker for string, if S3 not there start over
                #game Data
                gameData = temp
                ball = int(gameData[27:-20])
                ball = format(ball, ",d")
                ball = ('Ball: %s' % ball)
                players = int(gameData[16:-31]) # starts with 1
                players = format(players, ",d")
                players = ('Total Players: %s' % players)
                active_player = int(gameData[17:-30]) # starts at 0
                active_player_text = active_player + 1
                active_player_text = format(active_player_text, ",d")
                active_player_text = ('Player %s' % active_player_text)
                #score Data
                scoreData.split("=")[1].replace("]", "")
                scoreData = int(scoreData.split("=")[1].replace("]", ""), 16)
                scoreData = format(scoreData, ",d")
                state = temp
                state = state[20:-26]
                print state
                #text score, ball, players, and active player render code
                textScore = font.render(scoreData, True,(255,255,255))
                textScoreRect = textScore.get_rect()
                textScoreRect.center = (X // 2, 950)
                #render the score text
                textBall = font2.render(ball, True,(255,255,255))
                textBallRect = textBall.get_rect()
                textBallRect = (100, 940)
                textPlayers = font2.render(players, True,(255,255,255))
                textPlayersRect = textPlayers.get_rect()
                textPlayersRect = (100, 980)
                textActivePlayer = font2.render(active_player, True,(255,255,255))
                textActivePlayerRect = textActivePlayer.get_rect()
                textActivePlayerRect.center =(X // 2, 1000)


                if len(playerFlags)-1 < players:
                    playerFlags = list( dict(golden_flags) for i in range(players+1) )

                flags = playerFlags[active_player]
                globalFlags = playerFlags[len(playerFlags)-1]

                if (players != 1):
                    #single player games mean nothing to us so just keep going.
                    if (globalFlags['ball_end']):
                        #the ball has ended
                        if (active_player != globalFlags['ball_end_player']):
                            #we are no longer on the same player
                            globalFlags['ball_end'] = False
                            if flags['default_state_run']:
                                state = flags['default_state']
                                logger.info("Running the default state of %s" % state)
                                flags['default_state_run'] = False
                        else:
                            # sending back to ball drain
                            state = '19'

                if '01' in state:
                    if not globalFlags['attract_mode_active']:
                        logger.info("Attract is running")
                        result = filechecker(True, 'a', '/media/usb1/attract/attract.mp4')
                        logger.debug(result)
                        logger.info("setting attract mode %s" % result)
                        #globalFlags = dict.fromkeys(modelist, False)
                        globalFlags['attract_mode_active'] = True
                        #playerFlags = list()
                        break
                    else:
                        logger.debug("attract already running")

                elif '61' in state: #moved from 61 to 68 for LE
                        #Default state if bank is up
                        logger.info("Game Started - Player %s. Play Enter the Grid / default video being set to game_start" % active_player)
                        globalFlags['attract_mode_active'] = False
                        if not flags['null_mode_active']:
                            result = filechecker(True, 'a', '/media/usb1/attract/game_start.mp4')
                            logger.debug(result)
                            logger.info("Enter The Grid Video Playing %s" % result)
                            flags = dict.fromkeys(modelist, False)
                            flags['null_mode_active'] = True
                            flags['default_state'] = '61'
                            logger.info("Set the default state to %s" % state)


                elif '67' in state: #move from 67 to 6B for LE
                        #Needs to be default state if bank is not down
                        logger.info("Spinning Disc Shot - Bank Down / Default Video being set to discmb_lit")
                        if not flags['discmb_lit']:
                            result = filechecker(True, 'a', '/media/usb1/discmb/discmb_lit.mp4')
                            logger.debug(result)
                            logger.info("played disc mblit video - bank down")
                            logger.debug(result)
                            flags['discmb_lit'] = True
                            flags['discmb_active'] = False
                            flags['discmb_complete'] = False
                            flags['discmb_restart'] = False
                            flags['discmb_return'] = False
                            flags['recog_hit'] = False
                            flags['default_state'] = '67'
                            logger.info("Set the default state to %s" % state)

                elif '26' in state:
                        logger.info("game over")
                        if not flags['game_over']:
                            result = filechecker(True, 'I', '/media/usb1/attract/game_over.mp4')
                            logger.debug(result)
                               #we do this first so we can handle the game over looping until the next player starts OR the video terminates and we go back to attract mode
                            flags = dict.fromkeys(modelist, False)
                            flags['game_over'] = True
                            flags['null_mode_active'] = False

                elif '5D' in state:
                        logger.info("zen")
                        if not flags['zen']:
                            result = filechecker(False, 'I', '/media/usb1/flynn/zen.mp4')
                            logger.debug(result)
                            flags['zen'] = True

                elif '83' in state:
                        logger.info("flynn lit")
                        if not flags['flynn_lit']:
                            result = filechecker(False, 'I', '/media/usb1/flynn/flynn_lit.mp4')
                            logger.debug(result)
                            flags['flynn_lit'] = True
                            flags['flynn_complete'] = False

                elif '84' in state:
                        logger.info("flynn complete")
                        if not flags['flynn_complete']:
                            result = filechecker(False, 'I', '/media/usb1/flynn/flynn_complete.mp4')
                            logger.debug(result)
                            flags['flynn_complete'] = True
                            flags['flynn_lit'] = False

                elif '66' in state: # moved from 66 to 6C
                        logger.info("Recognizer Hit / Setting default base video to recognizer_hit")
                        if not flags['recog_hit']:
                            result = filechecker(True, 'a', '/media/usb1/recognizer/recognizer_hit.mp4')
                            logger.debug(result)
                            flags['recog_hit'] = True
                            flags['zen'] = False
                            flags['default_state'] = '66'
                            logger.info("Set the default state to %s" % state)

                elif '49' in state:
                        logger.info("clu lit")
                        if not flags['clu_lit']:
                            result = filechecker(False, 'I', '/media/usb1/clu/clu_lit.mp4')
                            logger.debug(result)
                            flags['clu_lit'] = True
                            flags['clu_active'] = False
                            flags['clu_complete'] = False

                elif '40' in state:
                        logger.info("clu active")
                        if not flags['clu_active']:
                            result = filechecker(False, 'I', '/media/usb1/clu/clu_active.mp4')
                            logger.debug(result)
                            flags['clu_active'] = True
                            flags['clu_lit'] = False
                            flags['clu_complete'] = False

                elif '43' in state:
                        logger.info("clu complete")
                        if not flags['clu_complete']:
                            result = filechecker(False, 'I', '/media/usb1/clu/clu_complete.mp4')
                            logger.debug(result)
                            flags['clu_complete'] = True
                            flags['clu_active'] = False
                            flags['clu_lit'] = False

                elif '2E' in state:
                        logger.info("discmb_active / appending but not clearing the discmb_active video")
                        if not flags['discmb_active']:
                            result = filechecker(True, 'a', '/media/usb1/discmb/discmb_active.mp4')
                            logger.debug(result)
                            flags['discmb_complete'] = False
                            flags['discmb_lit'] = False
                            flags['discmb_active'] = True
                            flags['recog_hit'] = False

                elif '34' in state:
                        logger.info("discmb_restart inserting discmb_restart and then setting L for game_start")
                        if not flags['discmb_restart']:
                            result = filechecker(True, 'I', '/media/usb1/discmb/discmb_restart.mp4')
                            logger.debug(result)
                            time.sleep(1)
                            result = filechecker(False, 'L', '/media/usb1/attract/game_start.mp4')
                            logger.debug(result)
                            flags['discmb_restart'] = True
                            flags['discmb_lit'] = False
                            flags['discmb_active'] = False
                            flags['discmb_return'] = False
                            flags['default_state'] = '61'

                elif '36' in state:
                        logger.info("discmb_return / setting discmb_active as the default video and clearing playlist")
                        if not flags['discmb_return']:
                            result = filechecker(True, 'a', '/media/usb1/discmb/discmb_active.mp4')
                            logger.debug(result)
                            flags['discmb_return'] = True
                            flags['discmb_complete'] = False
                            flags['discmb_lit'] = False
                            flags['discmb_active'] = True
                            flags['recog_hit'] = False

                elif '33' in state:
                        logger.info("discmb_complete / clearing playlist, inserting discmb_complete and then L for game_start")
                        if not flags['discmb_complete']:
                            result = filechecker(True, 'I', '/media/usb1/discmb/discmb_complete.mp4')
                            logger.debug(result)
                            time.sleep(1)
                            result = filechecker(False, 'L', '/media/usb1/attract/game_start.mp4')
                            logger.debug(result)
                            flags['discmb_complete'] = True
                            flags['discmb_active'] = False
                            flags['discmb_lit'] = False
                            flags['discmb_restart'] = False
                            flags['discmb_return'] = False
                            flags['default_state'] = '61'
                #TRON DISABLED FOR NOW
                elif '65' in state:
                        logger.info("tron_active / do nothing")
                        if not flags['tron_active']:
                            #result = filechecker(False, 'I', '/media/usb1/tron/tron_active.mp4')
                            #logger.debug(result)
                            flags['tron_active'] = True
                            flags['tron_complete'] = False
                #TRON DISABLED FOR NOW
                elif '64' in state:
                        logger.info("tron_complete / do nothing")
                        if not flags['tron_complete']:
                            #result = filechecker(False, 'I', '/media/usb1/tron/tron_complete.mp4')
                            #logger.debug(result)
                            #Could add multiple if not flags so that this doesn't fire when active modes are running
                            flags['tron_complete'] = True
                            flags['tron_active'] = False

                elif '45' in state:
                        logger.info("gem_active / insert gem_active video")
                        if not flags['gem_active']:
                            result = filechecker(False, 'I', '/media/usb1/gem/gem_active.mp4')
                            logger.debug(result)
                            flags['gem_active'] = True
                            flags['gem_complete'] = False

                elif '48' in state:
                        logger.info("gem_complete / insert gem_complete video")
                        if not flags['gem_complete']:
                            result = filechecker(False, 'I', '/media/usb1/gem/gem_complete.mp4')
                            logger.debug(result)
                            flags['gem_complete'] = True
                            flags['gem_active'] = False

                elif '57' in state:
                        logger.info("zuse_active")
                        if not flags['zuse_active']:
                            result = filechecker(False, 'I', '/media/usb1/zuse/zuse_active.mp4')
                            logger.debug(result)
                            flags['zuse_active'] = True
                            flags['zuse_complete'] = False

                elif '5C' in state:
                        logger.info("zuse_complete")
                        if not flags['zuse_complete']:
                            result = filechecker(False, 'I', '/media/usb1/zuse/zuse_complete.mp4')
                            logger.debug(result)
                            flags['zuse_complete'] = True
                            flags['zuse_active'] = False

                elif '4D' in state:
                        logger.info("lcmb_lit")
                        if not flags['lcmb_lit']:
                            result = filechecker(False, 'I', '/media/usb1/lcmb/lcmb_lit.mp4')
                            logger.debug(result)
                            flags['lcmb_lit'] = True
                            flags['lcmb_active'] = False
                            flags['lcmb_complete'] = False

                elif '4E' in state:
                        logger.info("lcmb_active")
                        if not flags['lcmb_active']:
                            result = filechecker(False, 'I', '/media/usb1/lcmb/lcmb_active.mp4')
                            logger.debug(result)
                            flags['lcmb_active'] = True
                            flags['lcmb_complete'] = False
                            flags['lcmb_lit'] = False

                elif '53' in state:
                        logger.info("lcmb_complete")
                        if not flags['lcmb_complete']:
                            result = filechecker(False, 'I', '/media/usb1/lcmb/lcmb_complete.mp4')
                            logger.debug(result)
                            flags['lcmb_complete'] = True
                            flags['lcmb_lit'] = False
                            flags['lcmb_active'] = False

                elif '38' in state:
                        logger.info("qmb_lit")
                        if not flags['qmb_lit']:
                            result = filechecker(False, 'I', '/media/usb1/qmb/qmb_lit.mp4')
                            logger.debug(result)
                            flags['qmb_lit'] = True
                            flags['qmb_active'] = False
                            flags['qmb_complete'] = False

                elif '39' in state:
                        logger.info("qmb_active")
                        if not flags['qmb_active']:
                            result = filechecker(False, 'a', '/media/usb1/qmb/qmb_active.mp4')
                            logger.debug(result)
                            flags['qmb_active'] = True
                            flags['qmb_lit'] = False
                            flags['qmb_complete'] = False

                elif '3F' in state:
                        logger.info("qmb_complete")
                        if not flags['qmb_complete']:
                            result = filechecker(False, 'I', '/media/usb1/qmb/qmb_complete.mp4')
                            logger.debug(result)
                            flags['qmb_complete'] = True
                            flags['qmb_lit'] = False
                            flags['qmb_active'] = False

                elif '6B' in state:
                        logger.info("sos_lit")
                        if not flags['sos_lit']:
                            result = filechecker(False, 'I', '/media/usb1/sos/sos_lit.mp4')
                            logger.debug(result)
                            flags['sos_lit'] = True
                            flags['sos_active'] = False
                            flags['sos_complete'] = False

                elif '6C' in state:
                        logger.info("sos_active")
                        if not flags['sos_active']:
                            result = filechecker(True, 'a', '/media/usb1/sos/sos_active.mp4')
                            logger.debug(result)
                            flags['sos_active'] = True
                            flags['sos_lit'] = False
                            flags['sos_complete'] = False

                elif '78' in state:
                        logger.info("sos_complete")
                        if not flags['sos_complete']:
                            result = filechecker(True, 'I', '/media/usb1/zuse/sos_complete.mp4')
                            logger.debug(result)
                            time.sleep(1)
                            result = filechecker(False, 'L', '/media/usb1/attract/game_start.mp4')
                            logger.debug(result)
                            flags['sos_complete'] = True
                            flags['sos_lit'] = False
                            flags['sos_active'] = False

                elif '87' in state:
                        logger.info("portal_active")
                        if not flags['portal_active']:
                            result = filechecker(True, 'a', '/media/usb1/portal/portal_active.mp4')
                            logger.debug(result)
                            flags['portal_active'] = True
                            flags['portal_complete'] = False

                elif '8C' in state:
                        logger.info("portal_complete")
                        if not flags['portal_complete']:
                            result = filechecker(True, 'I', '/media/usb1/portal/portal_complete.mp4')
                            logger.debug(result)
                            time.sleep(1)
                            result = filechecker(False, 'L', '/media/usb1/attract/game_start.mp4')
                            logger.debug(result)
                            flags['portal_active'] = False
                            flags['portal_complete'] = True

                elif '00' in state:
                    logger.info("No Active States")

                elif '19' in state:
                    logger.info("Player %s Ball Ended / Clearing Active modes and Complete modes" % active_player)
                    flags['discmb_active'] = False
                    flags['discmb_complete'] = False
                    flags['clu_active'] = False
                    flags['clu_complete'] = False
                    flags['gem_active'] = False
                    flags['gem_complete'] = False
                    flags['zuse_active'] = False
                    flags['zuse_complete'] = False
                    flags['lcmb_active'] = False
                    flags['lcmb_complete'] = False
                    flags['qmb_active'] = False
                    flags['qmb_complete'] = False
                    flags['sos_active'] = False
                    flags['sos_complete'] = False
                    flags['portal_active'] = False
                    flags['portal_complete'] = False
                    flags['default_state_run'] = True
                    flags[default_state_map[flags['default_state']]] = False
                    globalFlags['ball_end'] = True
                    globalFlags['ball_end_player'] = active_player

                    logger.info("we just set %s to %s" % (default_state_map[flags['default_state']], flags[default_state_map[flags['default_state']]]))
                    #time.sleep(1)

                else:
                    logger.info("new unhandled state %s" % state.rstrip())

                playerFlags[active_player] = flags
            screen.blit(textBall, textBallRect)
            screen.blit(textActivePlayer, textActivePlayerRect)
            screen.blit(textPlayers, textPlayersRect)
            screen.blit(textScore, textScoreRect)
            pygame.display.update()   # Call this only once per loop
            clock.tick(fps)     # forces the program to run at 30 fps.

    except serial.SerialException as str_error:
        serialport.close()
        strError = str(str_error)
        logger.info ("Error communicating with Serial Interface")
        logger.error("%s" % strError.rstrip())
        result = filechecker(False, 'I', '/media/usb1/system/serial_failure.mp4')
        time.sleep(10)  # wait for 10 seconds before trying to fetch the data again
        pass
