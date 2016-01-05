from stream.video_stream import VideoStream 
from umanager import UManager
import roboticsnet
from roboticsnet.command_validator import *


class Commands:
    def __init__(self):
        self.umanager = self.webcam_stream = None
        try:
            self.uManager = UManager()
        except Exception as e:
            print e.message
        
        try:
            self.webcam_stream = VideoStream('/dev/video0',8081)
        except Exception as e:
            print e.message

    def execute(bytes):
        cmd = ord(bytes[0])
        
        if cmd in range(0x01,0x07):
            value = ord(bytes[1])
            timediff = ord(calculate_time_diff(bytes[2]))
        
        
        if cmd == ROBOTICSNET_DRIVE_FORWARD:
            self.umanager.forward({'value':value, 'timediff':timediff})
            
        elif cmd == ROBOTICSNET_DRIVE_REVERSE:
            self.umanager.reverse({'value':value, 'timediff':timediff})
        
        elif cmd == ROBOTICSNET_DRIVE_FORWARDLEFT:
            self.umanager.forwardleft({'value':value, 'timediff':timediff})
        
        elif cmd == ROBOTICSNET_DRIVE_FORWARDRIGHT:
            self.umanager.forwardright({'value':value, 'timediff':timediff})
        
        elif cmd == ROBOTICSNET_DRIVE_REVERSELEFT:
            self.umanager.reverseleft({'value':value, 'timediff':timediff})
        
        elif cmd == ROBOTICSNET_DRIVE_REVERSERIGHT:
            self.umanager.reverseright({'value':value, 'timediff':timediff})
        
        elif cmd == ROBOTICSNET_DRIVE_STOP:
            self.umanager.stop({'timediff':ord(calculate_time_diff(bytes[1]))})
        
        elif cmd == ROBOTICSNET_CAMERA_START_VID:
            self.webcam_stream.start()
        
        elif cmd == ROBOTICSNET_CAMERA_START_VID:
            self.webcam_stream.end()
        
        elif cmd == ROBOTICSNET_CAMERA_SNAPSHOT:
            pass
        
        elif cmd == ROBOTICSNET_CAMERA_PANORAMICSNAPSHOT:
            pass
        
        
            
            
            
                    
