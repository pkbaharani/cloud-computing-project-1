import picamera
from time import sleep
import time

camera = picamera.PiCamera()
camera.start_preview()
time_str = time.strftime("%Y%m%d_%H%M%S")
camera.start_recording(time_str + '.h264')
camera.wait_recording(10)
camera.stop_recording()
camera.stop_preview()
