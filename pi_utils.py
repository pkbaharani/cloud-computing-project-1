import picamera
from time import sleep
import time

STATUS_FILE="./pi_status.txt"
INPUT_FILE = "./Input_Videos/{}.h264"

def record_video(duration):
	 
	camera = picamera.PiCamera()
	
	# Remove if ssh throws GUI error
	camera.start_preview()
	
	file_path = INPUT_FILE.format(time.strftime("%Y%m%d_%H%M%S"))
	camera.start_recording(file_path, format="h264")
	camera.wait_recording(duration)
	camera.stop_recording()
	
	# Remove if ssh throws GUI error
	camera.stop_preview()
	camera.close()
	return file_path
	
	
def is_busy():
	with open("./pi_status.txt", "r") as file_ptr:
		status = file_ptr.readline()
	if status == "0":
		return False
	return True
	
def set_busy():
	with open(STATUS_FILE, "w+") as file_ptr:
		file_ptr.write("1")

def set_free():
	with open(STATUS_FILE, "w+") as file_ptr:
		file_ptr.write("0")
