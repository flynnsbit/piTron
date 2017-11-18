#!/bin/sh

dd if=/dev/zero of=/dev/fb0 
echo X > /var/run/omxctl
echo O -b > /var/run/omxctl
echo O --no-osd > /var/run/omxctl
#echo A /home/pi/media/attract/Z-Stern-Repeat.mp4 > /var/run/omxctl
dd if=/dev/zero of=/dev/fb0
python /home/pi/ogtron.pyc
