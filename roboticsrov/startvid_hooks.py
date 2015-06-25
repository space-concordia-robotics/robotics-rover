#!/usr/bin/env python2.7

import os
import roboticsnet
from roboticsnet.command_hook import CommandHook
from roboticsnet.rover_listener import RoverListener

def _startVideo():
	os.system("killall vlc")
	print "This is the startvid hook!"

# First you would need to define your hooks using CommandHook
cmd_hook = CommandHook(
        startVideo=_startVideo
        )

l = RoverListener(hooks=cmd_hook)

print roboticsnet.__appname__, " ",  roboticsnet.__version__
print "Starting command dispatcher..."
l.listen()
