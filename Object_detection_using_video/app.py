import argparse
import os
from Ambiancer import *
from Utils import *
from Config import *

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
ap.add_argument("-c", "--config_path", required=True,
	help="config yaml path")
ap.add_argument("-d", "--ml_detector_algo", type=str, default="hog",
	help="choose yolo or hog")
args = vars(ap.parse_args())

config = Config(load_yaml(args["config_path"]))
light_pos_file_path = args["light_pos_file"]
metadata_file_path = args["metadata"]
detector = args["ml_detector_algo"]

print(detector)
ambiancer = Ambiancer(config, light_pos_file_path, metadata_file_path, detector)

ambiancer.start_stream_proc(args["input"], args["output"])

ambiancer.show_images(True)