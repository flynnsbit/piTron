#!/usr/bin/env python3

import serial
import time
import os
import pygame



serialport = serial.Serial("/dev/ttyUSB0", 57600, timeout=0.5)

class pyscore :
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
#        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
#        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pygame.font.init()
        # Render the screen
 #?       pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
    
    def test(self):
        "Test method to make sure the display is configured correctly"
        adcColor = (255, 255, 0)  # Yellow
       # self.drawGraticule()
        # Render the Adafruit logo at 10,360
       # logo = pygame.image.load('tron_recognizer.gif').convert()
       # self.screen.blit(logo, (10, 335))
        # Get a font and use it render some text on a Surface.
        font = pygame.font.Font(None, 80)
        text_surface = font.render('%s' % score,  True, (255, 255, 255))  # White text
        # Blit the text at 10, 0
        self.screen.blit(text_surface, (850, 900))
        pygame.display.update()


while 1:
#	time.sleep(.5)
	#serialport.write("zc mod 0x54A05f40\n")  #mode states pull
        serialport.write("zc mod 0x5c073564 0\n")  #Score
 	response = serialport.readlines()
	void = response.pop(0)
	for temp in response:
#		ball = data[27:-20]
#		players = data[16:-31]
#		current_player = data [17:-30]
#		string = data[2:-4]
                state = temp
                if "=" in state:
                     #print state
                     state.split("=")[1].replace("]", "")
                     score=int(state.split("=")[1].replace("]", ""), 16)
      #              state = state[20:-26]
       #              print "-------------------------------"
       #              print "current score %s" % score
                     fscore = pyscore()
                     fscore.test()
#                else:
 #                    break







