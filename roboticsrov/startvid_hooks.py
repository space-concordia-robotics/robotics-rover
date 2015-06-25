#!/usr/bin/env python2.7

import os
import roboticsnet
from roboticsnet.command_hook import CommandHook
from roboticsnet.rover_listener import RoverListener

def _startVideo():
	os.system("killall vlc")
	print "Starting stream from startvid!"
	os.system("cvlc v4l:///dev/video0 --sout '#transcode{vcodec=mp4v,vb=800,acodec=mpga,ab=128}:standard{access=http,mux=ts,dst=:8080}'")

def _stopVideo():
	os.system("killall vlc")
	print "Stopping stream from stopvid!"

# First you would need to define your hooks using CommandHook
cmd_hook = CommandHook(
        startVideo=_startVideo
        stopVideo=_stopVideo
        )

l = RoverListener(hooks=cmd_hook)

print roboticsnet.__appname__, " ",  roboticsnet.__version__
print "Starting command dispatcher..."
l.listen()
