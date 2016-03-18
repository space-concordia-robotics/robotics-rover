from stream.video_stream import VideoStream
from umanager import UManager
import roboticsnet
from roboticsnet.command_validator import *
from roboticsnet.gateway_constants import *
from roboticsrov.camera.images import snapshot, panoramic



class Commands:
    def __init__(self, logger):
        self.umanager = self.webcam_stream = None
        self.log_conn = logger

        try:
            self.uManager = UManager()
        except Exception as e:
            self.log_conn.send(["err","Error initializing UManager!\n\t{0}".format(e.message)])

        try:
            self.webcam_stream = VideoStream('/dev/video0',8081)
        except Exception as e:
            self.log_conn.send(["err","Error initializing webcam stream!\n\t{0}".format(e.message)])

    def execute(self, bytes):
        cmd = ord(bytes[0])

        if cmd in range(0x01,0x07):
            value = ord(bytes[1])
            timediff = calculate_time_diff(ord(bytes[2]))

        if cmd == DRIVE_FORWARD:
            self.umanager.forward({'value':value, 'timediff':timediff})

        elif cmd == DRIVE_REVERSE:
            self.umanager.reverse({'value':value, 'timediff':timediff})

        elif cmd == DRIVE_LEFT:
            self.umanager.left({'value':value, 'timediff':timediff})
        
        elif cmd == DRIVE_RIGHT:
            self.umanager.right({'value':value, 'timediff':timediff})

        elif cmd == DRIVE_STOP:
            self.umanager.stop({'timediff':calculate_time_diff(ord(bytes[1]))})

        elif cmd == CAMERA_START_VID:
            self.webcam_stream.start()

        elif cmd == CAMERA_START_VID:
            self.webcam_stream.end()

        elif cmd == CAMERA_SNAPSHOT:
            path = snapshot()
            return path

        elif cmd == CAMERA_PANORAMICSNAPSHOT:
            path = panoramic()
            return path
