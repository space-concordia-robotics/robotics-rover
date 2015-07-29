import subprocess

VLC_ARGS = ['cvlc', 'v4l:///dev/video0', '--sout', '#transcode{vcodec=WMV2,vb=1500}:standard{access=http,mux=ts,dst=:8080}']

# Global var video_stream_process holds vlc Popen subprocess, streaming boolean maintains stream state 
video_stream_process = None
streaming = False

# Start vlc stream
def start_video():
	global video_stream_process, streaming
	if (streaming):
		print "Stream already running."
	else:	
		print "Starting stream..."
		video_stream_process = subprocess.Popen(VLC_ARGS)
		streaming = True

# Stop vlc stream
def stop_video():
	global video_stream_process, streaming
	if (streaming):
		print "Stopping stream..."
		video_stream_process.kill()
		streaming = False
	else:
		print "No stream to stop."
