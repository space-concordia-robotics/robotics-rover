import subprocess
from stream_constants import *

class VideoStream:
    """
    Video stream that is broadcast on the network on a specified port, using the program mjpg_streamer
    Once the stream is up, this can be accessed over http (as an MJPEG) at http://[rover host]:[port]/?action=stream
    """
    
    def __init__(self, device='/dev/video0', port=DEFAULT_STREAM_PORT):
        """
        Parameters:
            device - the webcam to stream from. Should be a string, ex. '/dev/video0'
            port - the port to stream over. Should be an integer.
        """
        self.device = device
        self.port = port
        self.streaming = False
        
        # Args to pass to subprocess - determined from arg string via shlex.split() 
        self.stream_args = ['mjpg_streamer', '-i', '/usr/local/lib/input_uvc.so -d ' + self.device + ' -n -f ' + str(STREAM_FRAMERATE) + ' -r ' + STREAM_RESOLUTION,
                        '-o', '/usr/local/lib/output_http.so -p ' + str(self.port) + ' -n']
            
    def __del__(self):
        if (self.streaming):
            self.end()

    def start(self):
        """
        Starts the stream broadcast.
        """
        if (self.streaming):
            print "Stream already up."
        else:
            print "Starting stream..."
            print self.stream_args
            self.stream = subprocess.Popen(self.stream_args)
            self.streaming = True

    def end(self):
        """
        Ends the stream broadcast..
        """
        if (self.streaming):
            print "Stopping stream..."
            self.stream.terminate()
            self.streaming = False
        else:
            print "No stream to terminate."
