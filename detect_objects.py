INPUT_VIDEOS = "./Input_Videos/{}"
OUTPUT_FOLDER = "./Detected_Outputs/{}.txt"
import Library.s3 as S3
import os
import sys
import subprocess
import time

def start(input_file_path, is_pi=False):
	if is_pi:
		import pi_utils
	#import pdb;pdb.set_trace()
	print(input_file_path)
	file_name = input_file_path.split("/")[-1]
	with open("./input.txt", "w+") as ip_file:
		ip_file.write(input_file_path)
	record_time = file_name.split(".")[0]
	command = ["./darknet", "detector", "demo" ,"cfg/coco.data", "cfg/yolov3-tiny.cfg", "yolov3-tiny.weights", "{}".format(input_file_path)]
	run_cmd = subprocess.run(command,stdout=subprocess.PIPE, universal_newlines=True)
	output=run_cmd.stdout
	err=run_cmd.stderr
	#output = command.read()


	clean_output = output.replace("\x1b[2J\x1b[1;1H", "")
	clean_output = clean_output.replace("\n\n", "\n")
	split_output = clean_output.split("\n")
	
	output_file_path = OUTPUT_FOLDER.format(file_name)
	with open(output_file_path, "w+") as op_file:
		for line in split_output[3:]:
			if len(line) > 0 and line.find("Objects") == -1 and line.find("FPS") == -1:
				obj = line.split(":")[0]
				op_file.write("({}, {})\n".format(record_time, obj))
				
	S3.upload_output_file(output_file_path)
	if is_pi:
		pi_utils.set_free()
	time.sleep(2)
	return output_file_path
	
	
	
			
			
			
