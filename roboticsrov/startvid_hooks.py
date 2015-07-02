#!/usr/bin/env python2.7

import subprocess
import roboticsnet
from roboticsnet.command_hook import CommandHook
from roboticsnet.rover_listener import RoverListener

videoStreamProcess = None
isStreaming = False

def _startVideo():
	global videoStreamProcess, isStreaming
	print "Starting stream from startvid!"
	isStreaming = True
	videoStreamProcess = subprocess.Popen(['cvlc', 'v4l:///dev/video0', '--sout', '#transcode{vcodec=WMV2,vb=1500}:standard{access=http,mux=ts,dst=:8080}'])

def _stopVideo():
	global videoStreamProcess, isStreaming
	if (isStreaming):
		print "Stopping stream from stopvid!"
		videoStreamProcess.kill()
		isStreaming = False
	else:
		print "No stream to stop!"

# First you would need to define your hooks using CommandHook
cmd_hook = CommandHook(
        startVideo=_startVideo,
        stopVideo=_stopVideo
        )

l = RoverListener(hooks=cmd_hook,default_port=8080)

print roboticsnet.__appname__, " ",  roboticsnet.__version__
print "Starting command dispatcher..."
l.listen()
