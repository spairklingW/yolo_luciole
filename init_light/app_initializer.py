# USAGE
# python yolo_video.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco

# import the necessary packages
import argparse
import imutils
from LightInitializerMock import *

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
args = vars(ap.parse_args())

light_initializer = LightInitializerMock()
light_initializer.detect_lights()
light_initializer.detect_lights_position()
light_initializer.print_light_position()