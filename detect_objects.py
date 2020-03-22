INPUT_VIDEOS = "./Saved_Videos/{}"
OUTPUT_FOLDER = "./Output/{}.txt"
import Library.s3 as S3

def start(input_file_path):
	file_name = input_file_path.split("/")[-1]
	
	command = os.popen("./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights {}".format(file_path))
	output = command.read()
	import pdb; pdb.set_trace()
	clean_output = output.replace("\x1b[2J\x1b[1;1H", "")
	clean_output = clean_output.replace("\n\n", "\n")
	split_output = clean_output.replace("\n")
	
	output_file_path = OUTPUT_FOLDER.format(file_name)
	with open(output_file_path, "w+") as op_file:
		for line in split_output[3:]:
			if len(line) > 0 and line.find("Objects") == -1 and line.find("FPS") == -1:
				obj = line.split(":")[0]
				op_file.write("({}, {})\n".format(record_time, obj))
				
	S3.upload_output_file(utput_file_path)
	pi_utils.set_free()
	return output_file_path
	
	
	
			
			
			
