import argparse
import os
from Ambiancer import *

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input video")
ap.add_argument("-o", "--output", required=True,
	help="path to output video")
ap.add_argument("-l", "--light_pos_file", required=True,
	help="path to output video")
ap.add_argument("-m", "--metadata", required=True,
	help="metadata interface file path")
ap.add_argument("-y", "--yolo", required=True,
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])
light_pos_file_path = args["light_pos_file"]
metadata_file_path = args["metadata"]

ambiancer = Ambiancer(labelsPath, weightsPath, configPath, light_pos_file_path, metadata_file_path)

ambiancer.start_stream_proc(args["input"], args["confidence"], args["threshold"], args["output"])

ambiancer.show_images(True)