import argparse
import os
import time
from Ambiancer import *
from Utils import *
from Config import *


def parse_args():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--mode", type=str, default="video",
                    help="choose between video and image input stream")
    ap.add_argument("-i", "--input", required=True,
                    help="path to input video")
    ap.add_argument("-o", "--output", required=False,
                        help="path to output video")
    ap.add_argument("-l", "--light_pos_file", required=True,
                    help="path to output video")
    ap.add_argument("-m", "--metadata", required=True,
                    help="metadata interface file path")
    ap.add_argument("-c", "--config_path", required=True,
                    help="config yaml path")
    ap.add_argument("-d", "--ml_detector_algo", type=str, default="hog",
                    help="choose yolo or hog")
    ap.add_argument("-f",  "--verbose", type=str, choices=['true', 'false'], default='false')
    args = vars(ap.parse_args())

    return args


def main():
    start_time = time.time()
    args = parse_args()
    config = Config(load_yaml(args["config_path"]))
    light_pos_file_path = args["light_pos_file"]
    metadata_file_path = args["metadata"]
    detector = args["ml_detector_algo"]
    mode = args["mode"]
    verbose = args["verbose"].lower() == "true"

    ambiancer = Ambiancer(config, light_pos_file_path, metadata_file_path, detector, verbose)

    if mode == "video":
        # TODO: check the file format
        ambiancer.start_stream_proc(args["input"], args["output"])
        ambiancer.show_images()
    else:
        # TODO: check the file format
        ambiancer.start_image_proc(args["input"])
        ambiancer.show_images()

    print("--- %s seconds ---" % (time.time() - start_time))

main()
