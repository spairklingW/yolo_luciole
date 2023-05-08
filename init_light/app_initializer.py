# USAGE
# python yolo_video.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco

# import the necessary packages
import argparse
import imutils
from LightInitializerMock import *
from Utils import *

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
args = vars(ap.parse_args())

light_initializer = LightInitializerMock()
light_initializer.detect_lights()
light_initializer.detect_lights_position()
lights_position = light_initializer.get_lights_position_as_list()

print("lights positions")
print(lights_position)

dump_yaml(lights_position, "light_pos.yaml")

debug = True
if debug:
    light_initializer.print_light_position()