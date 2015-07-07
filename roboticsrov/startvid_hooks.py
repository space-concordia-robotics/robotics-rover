#!/usr/bin/env python2.7

import subprocess
import roboticsnet
from roboticsnet.command_hook import CommandHook
from roboticsnet.rover_listener import RoverListener

# Global var videoStreamProcess holds vlc Popen subprocess, isStreaming boolean maintains stream state 
videoStreamProcess = None
isStreaming = False

# Start vlc stream
def _startVideo():
	global videoStreamProcess, isStreaming
	if (isStreaming):
		print "Stream already running."
	else:	
		print "Starting stream from startvid..."
		videoStreamProcess = subprocess.Popen(['cvlc', 'v4l:///dev/video0', '--sout', '#transcode{vcodec=WMV2,vb=1500}:standard{access=http,mux=ts,dst=:8080}'])
		isStreaming = True

# Stop vlc stream
def _stopVideo():
	global videoStreamProcess, isStreaming
	if (isStreaming):
		print "Stopping stream from stopvid..."
		videoStreamProcess.kill()
		isStreaming = False
	else:
		print "No stream to stop."

# Hook integration
cmd_hook = CommandHook(
        startVideo=_startVideo,
        stopVideo=_stopVideo
        )

l = RoverListener(hooks=cmd_hook,default_port=8080)

print roboticsnet.__appname__, " ",  roboticsnet.__version__
print "Starting stream command dispatcher..."
l.listen()
