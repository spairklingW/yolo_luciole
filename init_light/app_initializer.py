# USAGE
# python yolo_video.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco

# import the necessary packages
import argparse
from LightInitializerMock import *
from Utils import *

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
args = vars(ap.parse_args())

light_initializer = LightInitializerMock()
light_initializer.detect_lights()
light_initializer.detect_lights_position()
#lights_position = light_initializer.get_lights_position_as_list()
print("AAAAAAAHhhh")
lights_position = light_initializer.get_lights_rel_position_as_list()
metadata = light_initializer.get_metadata()

print("lights positions")
print(lights_position)
dump_yaml(lights_position, "light_pos.yaml")
dump_yaml(metadata, "metadata.yaml")

debug = True
if debug:
    light_initializer.print_light_position()